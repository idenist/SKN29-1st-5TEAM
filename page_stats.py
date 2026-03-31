import streamlit as st
import plotly.express as px
import pandas as pd
# 👈 utils.py에서 기존 함수와 신규 함수를 모두 불러옵니다.
from utils import load_car_data, load_yearly_car_data 

# ==========================================
# 1. 기존: 사용자 맞춤형 통계 화면 (carmaster_db)
# ==========================================
def show_stats():
    st.title("🚘 최근 5개월 자동차 신규 등록 통계")
    st.write("2025년 10월 ~ 2026년 2월 자동차 신규 등록 통계")
    st.markdown("---")

    df_car = load_car_data()

    if not df_car.empty:
        # 데이터 다듬기 (연령대 추가 등)
        fuel_dict = {'2': '경유', '5': '전기', '7': '하이브리드', '8': '휘발유'}
        vhcty_dict = {'1': '승용', '2': '승합', '3': '화물', '4': '특수'}
        
        df_car['연료명'] = df_car['use_fuel_code'].map(fuel_dict)
        df_car['차종명'] = df_car['vhcty_asort_code'].map(vhcty_dict)
        df_car['수집년월'] = df_car['regist_yy'] + "-" + df_car['regist_mt']
        df_car['연령대'] = df_car['agrde'] + "0대" 

        # ==========================================
        # Section 1: 카테고리별 비중 분석 (✨ 개편됨)
        # ==========================================
        st.subheader("🔍 1. 최근 5개월 분석")
        category_options = {
            '연료별 비중': '연료명',
            '차종별 비중': '차종명',
            '성별 비중': 'sexdstn',
            '연령대별 비중': '연령대',
            '국산/외산 비중': 'hmmd_imp_se_nm'
        }
        
        # 차트 선택 옵션을 없애고, 기준 선택 드롭다운만 깔끔하게 배치
        selected_label = st.selectbox("기준을 선택해주세요", list(category_options.keys()))
        selected_col = category_options[selected_label] 
            
        dynamic_summary = df_car.groupby(selected_col)['cnt'].sum().reset_index()
        dynamic_summary = dynamic_summary.rename(columns={'cnt': '등록대수'})
        
        # 1. 연료별 비중: 하이브리드와 전기를 입체적으로 강조 (Pie 차트)
        if selected_label == "연료별 비중":
            # 하이브리드와 전기에 해당하는 조각만 바깥으로 0.1만큼 빼냄 (pull)
            pull_values = [0.1 if val in ['하이브리드', '전기'] else 0 for val in dynamic_summary[selected_col]]
            
            fig1 = px.pie(dynamic_summary, values='등록대수', names=selected_col, 
                          title=f'✨ 전체 기간 {selected_label} (하이브리드·전기 강조)', hole=0.4)
            fig1.update_traces(pull=pull_values, textposition='inside', textinfo='percent+label')
            
        # 2. 차종별 비중: 승용 부분만 색을 넣고 나머지는 회색 처리 (Pie 차트)
        elif selected_label == "차종별 비중":
            color_map = {val: '#1f77b4' if val == '승용' else '#e5e5e5' for val in dynamic_summary[selected_col].unique()}
            
            fig1 = px.pie(dynamic_summary, values='등록대수', names=selected_col, 
                          title=f'✨ 전체 기간 {selected_label} (승용차 비중 강조)', hole=0.4,
                          color=selected_col, color_discrete_map=color_map)
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            
        # 3. 성별 비중: 확연히 대비되는 색상 지정 (Pie 차트)
        elif selected_label == "성별 비중":
            fig1 = px.pie(dynamic_summary, values='등록대수', names=selected_col, 
                          title=f'✨ 전체 기간 {selected_label}', hole=0.4,
                          color_discrete_sequence=['#1f77b4', '#ef553b']) # 파랑, 빨강 대비
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            
        # 4. 연령대별 비중: 깔끔한 디자인의 바 차트 
        elif selected_label == "연령대별 비중":
            dynamic_summary = dynamic_summary.sort_values(by=selected_col) # 연령대 순 정렬
            fig1 = px.bar(
                dynamic_summary,
                x=selected_col,
                y='등록대수',
                title=f'✨ 전체 기간 {selected_label}',
                text='등록대수'
            )
            fig1.update_traces(
                texttemplate='%{text:,.0f}', 
                textposition="outside",
                marker_color='#5B8FF9', # 세련된 블루
                opacity=0.9,
                width=0.55, # 막대 두께 살짝 얇게
                cliponaxis=False
            )
            fig1.update_layout(
                plot_bgcolor='white', 
                yaxis=dict(showgrid=True, gridcolor='#E5E7EB', zeroline=False, tickformat=',.0f'), 
                xaxis=dict(showgrid=False), 
                margin=dict(t=60), 
                showlegend=False
            )
            fig1.update_yaxes(range=[0, dynamic_summary['등록대수'].max() * 1.15]) # 상단 여백
            
        # 5. 국산/외산 비중: 확연히 대비되는 색상 지정 (Pie 차트)
        elif selected_label == "국산/외산 비중":
            fig1 = px.pie(dynamic_summary, values='등록대수', names=selected_col, 
                          title=f'✨ 전체 기간 {selected_label}', hole=0.4,
                          color_discrete_sequence=['#1f77b4', '#ff7f0e']) # 파랑, 주황 대비
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("---")

        # ==========================================
        # Section 2: 시간에 따른 변화 추이
        # ==========================================
        st.subheader("📅 2. 월별 분석")
        trend_label = st.selectbox(
            "카테고리를 선택하세요", 
            ["전체 합계"] + list(category_options.keys())
        )
        
        is_percentage_chart = False 

        if trend_label == "전체 합계":
            month_summary = df_car.groupby('수집년월')['cnt'].sum().reset_index().sort_values(by='수집년월')
            month_summary = month_summary.rename(columns={'cnt': '등록대수'})
            
            # 깔끔한 디자인의 꺾은선(Line) 그래프
            fig2 = px.line(
                month_summary, 
                x='수집년월', 
                y='등록대수', 
                title='월별 전체 신규 등록 대수 추이', 
                markers=True,
                text='등록대수'
            )
            
            fig2.update_traces(
                textposition="top center", 
                texttemplate='%{text:,.0f}',
                line=dict(color='#5B8FF9', width=3.5), 
                marker=dict(size=8, color='#5B8FF9', line=dict(width=2, color='white')), 
                cliponaxis=False 
            )
            
            fig2.update_layout(
                plot_bgcolor='white', 
                yaxis=dict(showgrid=True, gridcolor='#E5E7EB', zeroline=False), 
                xaxis=dict(showgrid=False), 
                margin=dict(t=60), 
                showlegend=False
            )
            
            y_min = month_summary['등록대수'].min()
            y_max = month_summary['등록대수'].max()
            fig2.update_yaxes(range=[y_min * 0.85, y_max * 1.15])
            
        else:
            trend_col = category_options[trend_label]
            month_summary = df_car.groupby(['수집년월', trend_col])['cnt'].sum().reset_index().sort_values(by='수집년월')
            month_summary = month_summary.rename(columns={'cnt': '등록대수'})

            # 1. 연료별 비중
            if trend_label == "연료별 비중":
                fig2 = px.bar(month_summary, x='수집년월', y='등록대수', color=trend_col, title=f'월별 {trend_label} 추이', barmode='group')
                fig2.update_layout(showlegend=True)

            # 2. 차종별 비중
            elif trend_label == "차종별 비중":
                is_percentage_chart = True
                month_summary['비율(%)'] = month_summary.groupby('수집년월')['등록대수'].transform(lambda x: x / x.sum() * 100)
                unique_vehicles = month_summary[trend_col].unique()
                v_color_map = {v: '#1f77b4' if v == '승용' else '#e5e5e5' for v in unique_vehicles}
                month_summary['text_label'] = month_summary['비율(%)'].apply(lambda x: f"{x:.1f}%" if x >= 5 else "")

                fig2 = px.bar(month_summary, x='수집년월', y='비율(%)', color=trend_col, 
                              title=f'월별 {trend_label} (승용차 비중 강조)', 
                              color_discrete_map=v_color_map, text='text_label')
                fig2.update_traces(textposition='inside', insidetextfont=dict(color='white'), selector=dict(type='bar'))
                fig2.update_layout(showlegend=True, barmode='stack')

            # 3. 성별 비중
            elif trend_label == "성별 비중":
                fig2 = px.bar(month_summary, x='수집년월', y='등록대수', color=trend_col, title=f'월별 {trend_label} 추이', barmode='group',
                              color_discrete_sequence=['#1f77b4', '#ef553b'], labels={trend_col: '성별'})
                fig2.update_layout(showlegend=True)

            # 4. 연령대별 비중
            elif trend_label == "연령대별 비중":
                is_percentage_chart = True
                month_summary['비율(%)'] = month_summary.groupby('수집년월')['등록대수'].transform(lambda x: x / x.sum() * 100)
                filtered_summary = month_summary[month_summary['비율(%)'] >= 10].copy()

                fig2 = px.bar(
                    filtered_summary, 
                    x='수집년월', 
                    y='비율(%)', 
                    color=trend_col, 
                    title=f'월별 {trend_label} (10% 이상 주요 항목)', 
                    text='비율(%)',
                    barmode='group' 
                ) 
                
                fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig2.update_layout(showlegend=True)

            # 5. 국산/외산 비중
            elif trend_label == "국산/외산 비중":
                fig2 = px.bar(month_summary, x='수집년월', y='등록대수', color=trend_col, title=f'월별 {trend_label} 추이', barmode='group',
                              color_discrete_sequence=['#1f77b4', '#ff7f0e'], labels={trend_col: '구분'})
                fig2.update_layout(showlegend=True)

            else:
                fig2 = px.bar(month_summary, x='수집년월', y='등록대수', color=trend_col, title=f'월별 {trend_label} 추이', barmode='group')
                fig2.update_layout(showlegend=True)

        # 공통 레이아웃 업데이트
        if is_percentage_chart:
            fig2.update_yaxes(title_text='비중 (%)', ticksuffix='%') 
        elif trend_label != "선택 안 함 (전체 합계만 보기)": 
            fig2.update_yaxes(tickformat=',.0f', title_text='등록대수')
            
        fig2.update_xaxes(type='category') 
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.warning("맞춤형 통계 데이터를 불러오지 못했습니다.")


# ==========================================
# 2. 신규: 연도별/용도별 등록 현황 화면 (vehicle_db_year)
# ==========================================
def show_yearly_stats():
    st.title("📈 연도별 자동차 등록 현황 (2017~2025)")
    st.write("연도별 전체 등록 추이와 관용/자가용/영업용 비중을 분석해 보세요!")
    st.markdown("---")

    df_yearly = load_yearly_car_data()

    if not df_yearly.empty:
        df_detail = df_yearly[df_yearly['vehicle_type'] != '총계']
        df_total = df_yearly[df_yearly['vehicle_type'] == '총계'].copy() 
        df_detail = df_detail.rename(columns={'reg_year': '연도'})
        df_detail = df_detail.rename(columns={'total_count': '등록대수'})
        
        st.subheader("📅 1. 연도별 자동차 등록 추이")
        
        trend_option = st.radio("추이 보기 방식", ["전체 합계 보기", "차종별로 나누어 보기"], horizontal=True)
        
        if trend_option == "전체 합계 보기":
            df_total['total_count_M'] = df_total['total_count'] / 1_000_000
            df_total['text_label'] = df_total['total_count_M'].apply(lambda x: f"{x:.1f}M")

            fig1 = px.line(
                df_total, x='reg_year', y='total_count', markers=True, 
                title='연도별 전체 누적 등록 대수',
                labels={'reg_year': '연도', 'total_count': '등록대수'}, 
                line_shape='spline'
            )
            
            fig1.update_traces(
                textposition="top center", line=dict(width=3.5), 
                marker=dict(size=8, line=dict(width=2, color='white')),
                hovertemplate="%{x}년: %{y:,.0f}대<extra></extra>" 
            )

            fig1.update_layout(template='plotly_white', margin=dict(l=10, r=10, t=50, b=10))
            fig1.update_xaxes(type='category', showgrid=False, title_font=dict(size=14, color='gray'), tickfont=dict(size=12, color='dimgray'))
            fig1.update_yaxes(
                showgrid=True, gridcolor='#F0F0F0', zeroline=False,
                title_font=dict(size=14, color='gray'), tickfont=dict(size=12, color='dimgray'),
                tickmode='linear', tick0=22000000, dtick=1000000, range=[21500000, 27500000] 
            )
        else:
            fig1 = px.bar(df_detail, x='연도', y='등록대수', color='vehicle_type', title='연도별 차종별 누적 등록 대수')
            fig1.update_xaxes(type='category')
            
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("---")

        st.subheader("🔍 2. 연도별 상세 비중 분석")
        
        year_list = sorted(df_detail['연도'].unique(), reverse=True)
        selected_year = st.selectbox("상세 분석을 원하시는 연도를 선택하세요", year_list)
        
        df_year = df_detail[df_detail['연도'] == selected_year]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**[{selected_year}년] 차종별 비중**")
            fig_pie1 = px.pie(df_year, values='등록대수', names='vehicle_type', hole=0.4)
            st.plotly_chart(fig_pie1, use_container_width=True)
            
        with col2:
            st.markdown(f"**[{selected_year}년] 용도별 비중 (관용/자가용/영업용)**")
            df_usage = pd.melt(df_year, id_vars=['vehicle_type'], 
                               value_vars=['official_count', 'private_count', 'business_count'], 
                               var_name='용도', value_name='등록수')
            
            usage_map = {'official_count': '관용', 'private_count': '자가용', 'business_count': '영업용'}
            df_usage['용도'] = df_usage['용도'].map(usage_map)
            
            usage_summary = df_usage.groupby('용도')['등록수'].sum().reset_index()
            fig_pie2 = px.pie(usage_summary, values='등록수', names='용도', hole=0.4, 
                              color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie2, use_container_width=True)

    else:
        st.warning("연도별 통계 데이터를 불러오지 못했습니다.")