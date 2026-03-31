import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_car_data, load_yearly_car_data

# 1. 사용자 맞춤형 통계 화면 (carmaster_db)
def show_stats():
    st.title("🚘 최근 5개월 자동차 신규 등록 통계")
    st.write("2025년 10월 ~ 2026년 2월 자동차 신규 등록 통계")
    st.markdown("---")

    df_car = load_car_data()

    if not df_car.empty:
        # 데이터 전처리
        fuel_dict = {'2': '경유', '5': '전기', '7': '하이브리드', '8': '휘발유'}
        vhcty_dict = {'1': '승용', '2': '승합', '3': '화물', '4': '특수'}
        
        df_car['연료명'] = df_car['use_fuel_code'].map(fuel_dict)
        df_car['차종명'] = df_car['vhcty_asort_code'].map(vhcty_dict)
        df_car['수집년월'] = df_car['regist_yy'] + "-" + df_car['regist_mt']
        df_car['연령대'] = df_car['agrde'] + "0대"

        # Section 1: 카테고리별 비중 분석
        st.subheader("🔍 1. 항목별 분석")
        category_options = {
            '연료별': '연료명',
            '차종별': '차종명',
            '성별': 'sexdstn',
            '연령대별': '연령대',
            '국산/외산': 'hmmd_imp_se_nm'
        }
        
        selected_label = st.selectbox("기준을 선택해주세요", list(category_options.keys()))
        selected_col = category_options[selected_label]
        dynamic_summary = df_car.groupby(selected_col)['cnt'].sum().reset_index().rename(columns={'cnt': '등록대수'})
        
        if selected_label == "연료별":
            pull_values = [0.1 if val == '하이브리드' else 0 for val in dynamic_summary[selected_col]]
            fig1 = px.pie(dynamic_summary, values='등록대수', names=selected_col, title=f'✨ 전체 기간 {selected_label}', hole=0.4)
            fig1.update_traces(pull=pull_values, textposition='inside', textinfo='percent+label')
        elif selected_label == "차종별":
            color_map = {val: '#1f77b4' if val == '승용' else '#e5e5e5' for val in dynamic_summary[selected_col].unique()}
            fig1 = px.pie(dynamic_summary, values='등록대수', names=selected_col, title=f'✨ 전체 기간 {selected_label}', hole=0.4, color=selected_col, color_discrete_map=color_map)
            fig1.update_traces(textposition='inside', textinfo='percent+label')
        elif selected_label == "성별":
            fig1 = px.pie(dynamic_summary, values='등록대수', names=selected_col, title=f'✨ 전체 기간 {selected_label}', hole=0.4, color_discrete_sequence=['#1f77b4', '#ef553b'])
            fig1.update_traces(textposition='inside', textinfo='percent+label')
        elif selected_label == "연령대별":
            dynamic_summary = dynamic_summary.sort_values(by=selected_col)
            fig1 = px.bar(dynamic_summary, x=selected_col, y='등록대수', title=f'✨ 전체 기간 {selected_label}', text='등록대수')
            fig1.update_traces(texttemplate='%{text:,.0f}', textposition="outside", marker_color='#5B8FF9', opacity=0.9, width=0.55, cliponaxis=False)
            fig1.update_layout(plot_bgcolor='white', yaxis=dict(showgrid=True, gridcolor='#E5E7EB', zeroline=False), xaxis=dict(showgrid=False), showlegend=False)
            fig1.update_yaxes(range=[0, dynamic_summary['등록대수'].max() * 1.15])
        elif selected_label == "국산/외산":
            fig1 = px.pie(dynamic_summary, values='등록대수', names=selected_col, title=f'✨ 전체 기간 {selected_label}', hole=0.4, color_discrete_sequence=['#1f77b4', '#ff7f0e'])
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("---")

        # Section 2: 각 항목 월별 분석 
        st.subheader("📅 2. 각 항목 월별 분석")
        trend_label = st.selectbox("카테고리를 선택하세요", ["전체 합계"] + list(category_options.keys()))
        
        is_percentage_chart = False

        if trend_label == "전체 합계":
            month_summary = df_car.groupby('수집년월')['cnt'].sum().reset_index().sort_values(by='수집년월').rename(columns={'cnt': '등록대수'})
            fig2 = px.line(month_summary, x='수집년월', y='등록대수', title='각 항목 월별 신규 등록 대수 추이', markers=True, text='등록대수')
            fig2.update_traces(textposition="top center", texttemplate='%{text:,.0f}', line=dict(color='#5B8FF9', width=3.5))
            fig2.update_layout(plot_bgcolor='white', showlegend=False)
            
        else:
            trend_col = category_options[trend_label]
            month_summary = df_car.groupby(['수집년월', trend_col])['cnt'].sum().reset_index().sort_values(by='수집년월').rename(columns={'cnt': '등록대수'})

            if trend_label == "연료별":
                fig2 = px.bar(month_summary, x='수집년월', y='등록대수', color=trend_col, title=f'월별 {trend_label} 분석', barmode='group')
            elif trend_label == "차종별":
                is_percentage_chart = True
                month_summary['비율(%)'] = month_summary.groupby('수집년월')['등록대수'].transform(lambda x: x / x.sum() * 100)
                fig2 = px.bar(month_summary, x='수집년월', y='비율(%)', color=trend_col, title=f'월별 {trend_label} 분석', barmode='stack')
            elif trend_label == "성별":
                fig2 = px.bar(month_summary, x='수집년월', y='등록대수', color=trend_col, title=f'월별 {trend_label} 분석', barmode='group', color_discrete_sequence=['#1f77b4', '#ef553b'])
            
            # 연령대별 월별 분석
            elif trend_label == "연령대별":
                is_percentage_chart = True
                month_summary['비율(%)'] = month_summary.groupby('수집년월')['등록대수'].transform(lambda x: x / x.sum() * 100)
                filtered_summary = month_summary[month_summary['비율(%)'] >= 10].copy()
                
                # 각 월별 1등 여부 확인
                filtered_summary['is_top'] = filtered_summary.groupby('수집년월')['비율(%)'].transform(lambda x: x == x.max())
                
                # 1등만 볼드 처리
                filtered_summary['bold_text'] = filtered_summary.apply(
                    lambda x: f"<b>{x['비율(%)']:.1f}%</b>" if x['is_top'] else f"{x['비율(%)']:.1f}%", axis=1
                )

                fig2 = px.bar(
                    filtered_summary,
                    x='수집년월',
                    y='비율(%)',
                    color=trend_col,
                    title=f'월별 {trend_label} 분석 (항목별 1등 강조)',
                    text='bold_text',
                    barmode='group'
                )
                fig2.update_traces(textposition='outside', cliponaxis=False)
            
            elif trend_label == "국산/외산":
                fig2 = px.bar(month_summary, x='수집년월', y='등록대수', color=trend_col, title=f'월별 {trend_label} 분석', barmode='group', color_discrete_sequence=['#1f77b4', '#ff7f0e'])
            else:
                fig2 = px.bar(month_summary, x='수집년월', y='등록대수', color=trend_col, title=f'월별 {trend_label} 분석', barmode='group')

        if is_percentage_chart:
            fig2.update_yaxes(title_text='비중 (%)', ticksuffix='%')
        elif trend_label != "전체 합계":
            fig2.update_yaxes(tickformat=',.0f', title_text='등록대수')
            
        fig2.update_xaxes(type='category')
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', legend_title_text='연령대')
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.warning("맞춤형 통계 데이터를 불러오지 못했습니다.")

# 2. 연도별/용도별 등록 현황 화면
def show_yearly_stats():
    st.title("📈 연도별 자동차 등록 현황 (2017~2025)")
    st.write("연도별 자동차 등록과 관용/자가용/영업용 비중 분석")
    st.markdown("---")

    df_yearly = load_yearly_car_data()

    if not df_yearly.empty:
        df_detail = df_yearly[df_yearly['vehicle_type'] != '총계']
        df_total = df_yearly[df_yearly['vehicle_type'] == '총계'].copy()
        df_detail = df_detail.rename(columns={'reg_year': '연도', 'total_count': '등록대수', 'vehicle_type': '차종'})
        
        min_year, max_year = df_total['reg_year'].min(), df_total['reg_year'].max()
        count_min = df_total[df_total['reg_year'] == min_year]['total_count'].values[0]
        count_max = df_total[df_total['reg_year'] == max_year]['total_count'].values[0]

        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("📅 1. 연도별 자동차 등록")
        with col2:
            st.markdown(f"<div style='text-align: right;'><div style='color: #555; font-size: 24px; font-weight: bold;'>{min_year}년 약 {count_min:,.0f}대 ➡️ {max_year}년 약 {count_max:,.0f}대</div></div>", unsafe_allow_html=True)
        
        trend_option = st.radio("추이 보기 방식", ["전체 합계 보기", "차종 비율 보기"], horizontal=True)
        
        if trend_option == "전체 합계 보기":
            fig_y = px.line(df_total, x='reg_year', y='total_count', markers=True, title='연도별 전체 누적 등록 대수')
            fig_y.update_yaxes(range=[21500000, 27500000])
        else:
            df_detail_sorted = df_detail.sort_values(by=['연도', '등록대수'], ascending=[True, False])
            fig_y = px.bar(df_detail_sorted, x='연도', y='등록대수', color='차종', title='연도별 차종 누적 등록 대수', color_discrete_sequence=['#1f77b4', '#6baed6', '#9ecae1', '#c6dbef'])
            
        st.plotly_chart(fig_y, use_container_width=True)
        st.markdown("---")
        
        st.subheader("🔍 2. 연도별 상세 분석")
        year_list = sorted(df_detail['연도'].unique(), reverse=True)
        selected_year = st.selectbox("연도 선택", year_list)
        df_year = df_detail[df_detail['연도'] == selected_year]
        
        c1, c2 = st.columns(2)
        with c1:
            fig_p1 = px.pie(df_year, values='등록대수', names='차종', hole=0.4, title=f'[{selected_year}] 차종별')
            fig_p1.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_p1, use_container_width=True)
        with c2:
            df_usage = pd.melt(df_year, id_vars=['차종'], value_vars=['official_count', 'private_count', 'business_count'], var_name='용도', value_name='등록수')
            usage_map = {'official_count': '관용', 'private_count': '자가용', 'business_count': '영업용'}
            df_usage['용도'] = df_usage['용도'].map(usage_map)
            usage_sum = df_usage.groupby('용도')['등록수'].sum().reset_index()
            fig_p2 = px.pie(usage_sum, values='등록수', names='용도', hole=0.4, title=f'[{selected_year}] 용도별', color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_p2.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_p2, use_container_width=True)
    else:
        st.warning("데이터 로드 실패")