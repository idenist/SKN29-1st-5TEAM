# page_traffic.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# 환경변수 및 DB 엔진 설정
load_dotenv()

@st.cache_resource
def get_db_engine():
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME_TRAFFIC", "traffic")
    
    url_object = URL.create(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name
    )
    
    return create_engine(url_object)

@st.cache_data
def load_traffic_data():
    engine = get_db_engine()
    query = "SELECT traffic_year, vehicle_class, traffic_volume FROM highway_traffic;"
    try:
        return pd.read_sql(query, con=engine)
    except Exception as e:
        st.error(f"데이터베이스 오류: {e}")
        return pd.DataFrame()

# 숫자를 'O억 O,OOO만' 형식으로 변환하는 헬퍼 함수
def format_korean_num(num):
    eok = int(num // 100_000_000)
    man = int((num % 100_000_000) // 10_000)
    
    if eok > 0:
        return f"{eok}억 {man:,}만" if man > 0 else f"{eok}억"
    return f"{man:,}만"

# ============================================
# 메인 파일에서 호출할 함수
# ============================================
def show_page():
    st.title("🚗 고속도로 통행량 추이")
    st.markdown("---")

    df = load_traffic_data()

    if not df.empty:
        # '합계' 데이터만 필터링
        df_total = df[df['vehicle_class'] == '합계'].copy()

        if not df_total.empty:
            # ✨ 1. 데이터 복원 및 단위 변환
            # 원본 데이터(천 대) -> 실제 대수 -> '억' 단위 변환
            df_total['actual_volume'] = df_total['traffic_volume'] * 1000
            df_total['traffic_Eok'] = df_total['actual_volume'] / 100_000_000

            # 연도별 통행량 변화 수치 계산
            min_year = df_total['traffic_year'].min()
            max_year = df_total['traffic_year'].max()
            
            min_vol = df_total[df_total['traffic_year'] == min_year]['actual_volume'].values[0]
            max_vol = df_total[df_total['traffic_year'] == max_year]['actual_volume'].values[0]
            diff_vol = max_vol - min_vol

            # 한국어 단위(억, 만)로 포맷팅
            min_text = format_korean_num(min_vol)
            max_text = format_korean_num(max_vol)
            diff_text = format_korean_num(diff_vol)

            # 상단 텍스트 레이아웃
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("📅 연도별 고속도로 통행량 변화")
            with col2:
                st.markdown(
                    f"<div style='text-align: right; padding-top: 1.0rem;'>"
                    f"<div style='color: #555; font-size: 24px; font-weight: bold;'>"
                    f"{min_year}년 약 {min_text}대 ➡️ {max_year}년 약 {max_text}대</div>"
                    f"<div style='color: #777; font-size: 18px; font-weight: normal; margin-top: 0.2rem;'>"
                    f"(총 {diff_text}대 증가)</div>"
                    f"</div>", 
                    unsafe_allow_html=True
                )

            # 차트 그리기
            fig = px.line(
                df_total,
                x='traffic_year',
                y='traffic_Eok',
                markers=True,
                line_shape='spline',
                labels={'traffic_year': '연도', 'traffic_Eok': '교통량 (단위: 억 대)'}
            )
            
            # 스타일 및 툴팁 적용
            fig.update_traces(
                line=dict(color='#08c7b4', width=3.5), 
                marker=dict(size=8, color='#08c7b4', line=dict(width=2, color='white')), 
                hovertemplate="%{x}년: %{y:.2f}억 대<extra></extra>" 
            )

            # 레이아웃 디자인
            fig.update_layout(
                template='plotly_white', 
                hovermode='x unified',  
                margin=dict(l=10, r=10, t=50, b=10) 
            )
            
            fig.update_xaxes(
                dtick=1, 
                showgrid=False, 
                title_font=dict(size=14, color='gray'),
                tickfont=dict(size=12, color='dimgray')
            )
            
            # ✨ 2. Y축 눈금 간격을 1.0(1억)으로 변경
            fig.update_yaxes(
                dtick=1.0,               # 눈금 간격을 1억 단위로 설정
                tickformat=".0f",        # 소수점 없이 정수로 표시 (17, 18, 19...)
                ticksuffix="억",          # 숫자 뒤에 '억' 접미사
                showgrid=True, 
                gridcolor='#F0F0F0', 
                zeroline=False,
                title_font=dict(size=14, color='gray'),
                tickfont=dict(size=12, color='dimgray')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("'합계' 데이터를 찾을 수 없습니다.")
    else:
        st.warning("데이터를 불러올 수 없습니다.")