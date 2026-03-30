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
    st.write("궁금한 조건을 직접 선택해서 나만의 맞춤형 통계를 확인해 보세요!")
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

        # Section 1: 카테고리별 비중 분석
        st.subheader("🔍 1. 카테고리별 비중 분석")
        category_options = {
            '연료별 비중': '연료명',
            '차종별 비중': '차종명',
            '성별 비중': 'sexdstn',
            '연령대별 비중': '연령대',
            '국산/외산 비중': 'hmmd_imp_se_nm'
        }
        
        col1, col2 = st.columns(2)
        with col1:
            selected_label = st.selectbox("어떤 기준의 통계를 보고 싶으신가요?", list(category_options.keys()))
            selected_col = category_options[selected_label] 
            
        with col2:
            chart_type = st.radio("차트 형태", ["파이 차트 🍩", "바 차트 📊"], horizontal=True)

        dynamic_summary = df_car.groupby(selected_col)['cnt'].sum().reset_index()
        
        if chart_type == "파이 차트 🍩":
            fig1 = px.pie(dynamic_summary, values='cnt', names=selected_col, title=f'✨ 전체 기간 {selected_label}', hole=0.4)
        else:
            dynamic_summary = dynamic_summary.sort_values(by='cnt', ascending=False)
            fig1 = px.bar(dynamic_summary, x=selected_col, y='cnt', title=f'✨ 전체 기간 {selected_label}', text_auto=True, color=selected_col)
            fig1.update_layout(showlegend=False) 
            
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("---")

        # Section 2: 시간에 따른 변화 추이
        st.subheader("📅 2. 시간에 따른 변화 추이")
        trend_label = st.selectbox(
            "추이를 세부적으로 나눠서 볼 기준을 선택하세요", 
            ["선택 안 함 (전체 합계만 보기)"] + list(category_options.keys())
        )
        
        if trend_label == "선택 안 함 (전체 합계만 보기)":
            month_summary = df_car.groupby('수집년월')['cnt'].sum().reset_index().sort_values(by='수집년월')
            fig2 = px.line(month_summary, x='수집년월', y='cnt', title='월별 전체 신규 등록 대수 추이', markers=True, text='cnt')
            fig2.update_traces(textposition="top center")
        else:
            trend_col = category_options[trend_label]
            month_summary = df_car.groupby(['수집년월', trend_col])['cnt'].sum().reset_index().sort_values(by='수집년월')
            fig2 = px.bar(month_summary, x='수집년월', y='cnt', color=trend_col, title=f'월별 {trend_label} 추이', text_auto=True, barmode='group')
        
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
        # 데이터 분리 (총계 행과 개별 차종 행 분리)
        df_detail = df_yearly[df_yearly['vehicle_type'] != '총계']
        df_total = df_yearly[df_yearly['vehicle_type'] == '총계']

        # Section 1: 연도별 등록 추이 (Line Chart)
        st.subheader("📅 1. 연도별 자동차 등록 추이")
        
        trend_option = st.radio("추이 보기 방식", ["전체 합계 보기", "차종별로 나누어 보기"], horizontal=True)
        
        if trend_option == "전체 합계 보기":
            fig1 = px.line(df_total, x='reg_year', y='total_count', markers=True, text='total_count', title='연도별 전체 누적 등록 대수')
            fig1.update_traces(textposition="top center")
        else:
            fig1 = px.bar(df_detail, x='reg_year', y='total_count', color='vehicle_type', title='연도별 차종별 누적 등록 대수')
            
        fig1.update_xaxes(type='category')
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("---")

        # Section 2: 특정 연도의 용도별/차종별 비중 분석
        st.subheader("🔍 2. 연도별 상세 비중 분석")
        
        year_list = sorted(df_detail['reg_year'].unique(), reverse=True)
        selected_year = st.selectbox("상세 분석을 원하시는 연도를 선택하세요", year_list)
        
        df_year = df_detail[df_detail['reg_year'] == selected_year]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**[{selected_year}년] 차종별 비중**")
            fig_pie1 = px.pie(df_year, values='total_count', names='vehicle_type', hole=0.4)
            st.plotly_chart(fig_pie1, use_container_width=True)
            
        with col2:
            st.markdown(f"**[{selected_year}년] 용도별 비중 (관용/자가용/영업용)**")
            df_usage = pd.melt(df_year, id_vars=['vehicle_type'], 
                               value_vars=['official_count', 'private_count', 'business_count'], 
                               var_name='용도', value_name='등록대수')
            
            usage_map = {'official_count': '관용', 'private_count': '자가용', 'business_count': '영업용'}
            df_usage['용도'] = df_usage['용도'].map(usage_map)
            
            usage_summary = df_usage.groupby('용도')['등록대수'].sum().reset_index()
            fig_pie2 = px.pie(usage_summary, values='등록대수', names='용도', hole=0.4, 
                              color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie2, use_container_width=True)

    else:
        st.warning("연도별 통계 데이터를 불러오지 못했습니다.")