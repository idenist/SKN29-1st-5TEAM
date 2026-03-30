# page_traffic.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# 환경변수 및 DB 엔진 설정은 함수 밖에 두어 재사용합니다.
load_dotenv()

@st.cache_resource
def get_db_engine():
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME_TRAFFIC", "traffic")
    
    # URL 객체를 사용하면 특수문자 파싱 에러를 원천 차단할 수 있습니다.
    url_object = URL.create(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_password,  # 알아서 안전하게 변환해 줌!
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

# ============================================
# 메인 파일에서 호출할 함수
# ============================================
def show_page():
    st.title("🚗 연도별 고속도로 통행량 추이")

    df = load_traffic_data()

    if not df.empty:
        vehicle_classes = df['vehicle_class'].unique()
        default_class = ['합계'] if '합계' in vehicle_classes else []
        
        selected_classes = st.multiselect(
            "확인하고 싶은 차종을 선택하세요:",
            options=vehicle_classes,
            default=default_class
        )

        filtered_df = df[df['vehicle_class'].isin(selected_classes)]

        if not filtered_df.empty:
            # === 여기서부터 디자인 수정됨 ===
            fig = px.line(
                filtered_df,
                x='traffic_year',
                y='traffic_volume',
                color='vehicle_class',
                markers=True,
                line_shape='spline', # 딱딱한 선 대신 부드러운 곡선 적용
                labels={'traffic_year': '연도', 'traffic_volume': '교통량(단위: 천)', 'vehicle_class': '차종'},
                color_discrete_sequence=px.colors.qualitative.Set1 # 좀 더 선명한 색상 팔레트 적용
            )
            
            # 선 굵기 및 마커 스타일 세부 조정
            fig.update_traces(
                line=dict(width=3.5), 
                marker=dict(size=8, line=dict(width=2, color='white')), 
                hovertemplate="%{y:,.0f}천 대<extra></extra>" # 숫자에 천 단위 콤마 추가
            )

            # 레이아웃 전반의 디자인 (배경, 그리드, 범례 위치)
            fig.update_layout(
                template='plotly_white', # 깔끔한 흰색 배경
                hovermode='x unified',   # 마우스를 올리면 해당 연도의 모든 차종 데이터를 툴팁 하나에 보여줌
                legend=dict(
                    orientation="h",     # 범례를 가로로 배치
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    title=None           # 범례의 '차종' 타이틀 생략 (공간 절약)
                ),
                margin=dict(l=10, r=10, t=50, b=10) # 불필요한 여백 최소화
            )
            
            # x, y축 디자인 깔끔하게 정리
            fig.update_xaxes(
                dtick=1, 
                showgrid=False, # x축 세로선 숨기기 (더 깔끔함)
                title_font=dict(size=14, color='gray'),
                tickfont=dict(size=12, color='dimgray')
            )
            fig.update_yaxes(
                showgrid=True, 
                gridcolor='#F0F0F0', # 연한 회색 가로선
                zeroline=False,
                title_font=dict(size=14, color='gray'),
                tickfont=dict(size=12, color='dimgray')
            )
            # === 여기까지 디자인 수정됨 ===
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("차종을 하나 이상 선택해주세요.")
    else:
        st.warning("데이터를 불러올 수 없습니다.")