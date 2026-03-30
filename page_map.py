import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# --- .env 로드 및 설정 ---
load_dotenv()
DB_HOST = os.getenv("DB_HOST", "127.0.0.1").strip().replace("@", "")
DB_PORT = os.getenv("DB_PORT", "3306").strip()
DB_USER = os.getenv("DB_USER", "root").strip()
DB_PWD  = os.getenv("DB_PASSWORD", "").strip()
DB_NAME_REST = os.getenv("DB_NAME_REST", "rest_area").strip()

@st.cache_resource
def get_rest_area_db_connection():
    try:
        from sqlalchemy.engine import URL
        connection_url = URL.create(
            drivername="mysql+pymysql",
            username=DB_USER,
            password=DB_PWD,
            host=DB_HOST,
            port=int(DB_PORT),
            database=DB_NAME_REST,
            query={"charset": "utf8mb4"}
        )
        return create_engine(connection_url)
    except Exception as e:
        st.error(f"⚠️ DB 연결 오류: {e}")
        return None

@st.cache_data
def load_all_rest_areas(_engine):
    if _engine is None: return pd.DataFrame()
    query = "SELECT restarea_name, route_name, xValue, yValue, service_area_code FROM rest_areas"
    try:
        return pd.read_sql_query(query, _engine)
    except Exception as e:
        st.error(f"⚠️ 데이터 로드 오류: {e}")
        return pd.DataFrame()

# ==========================================
# 메인 서비스 함수
# ==========================================
def show_rest_area_map():
    # 1. 헤더 디자인
    st.title("📍 고속도로 휴게소 탐색기")
    st.markdown("""
        전국 고속도로 휴게소의 위치를 노선별로 한눈에 확인하세요. 
        원하는 노선을 선택하면 해당 노선의 휴게소 리스트가 자동으로 업데이트됩니다.
    """)
    st.write("") # 공백

    engine = get_rest_area_db_connection()
    if not engine: return

    df = load_all_rest_areas(engine)
    if df.empty:
        st.warning("데이터가 존재하지 않습니다.")
        return

    # [중요] 데이터 타입 강제 변환 (문자열일 경우를 대비해 숫자로 변환)
    df['yValue'] = pd.to_numeric(df['yValue'], errors='coerce')
    df['xValue'] = pd.to_numeric(df['xValue'], errors='coerce')
    # NaN 값(잘못된 좌표) 제거
    df = df.dropna(subset=['yValue', 'xValue'])

    # 2. 필터 섹션
    all_routes = sorted(df['route_name'].unique().tolist())
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            default_val = ['경부선'] if '경부선' in all_routes else [all_routes[0]]
            selected_routes = st.multiselect("🗺️ 노선 선택", options=all_routes, default=default_val)
        with col2:
            filtered_df = df[df['route_name'].isin(selected_routes)].copy() # .copy() 추가
            st.metric("검색된 휴게소", f"{len(filtered_df)}개")

    st.markdown("---")

    if not filtered_df.empty:
        # 1. 데이터 타입 확인 및 마커 크기 설정
        filtered_df['yValue'] = pd.to_numeric(filtered_df['yValue'], errors='coerce')
        filtered_df['xValue'] = pd.to_numeric(filtered_df['xValue'], errors='coerce')
        filtered_df = filtered_df.dropna(subset=['yValue', 'xValue'])
        filtered_df['marker_size'] = 15 

        # 2. 지도 시각화 (고정된 center와 zoom 사용)
        fig = px.scatter_mapbox(
            filtered_df,
            lat="yValue",
            lon="xValue",
            hover_name="restarea_name",
            hover_data={"route_name": True, "yValue": False, "xValue": False, "marker_size": False},
            color="route_name",
            # --- [수정] 다시 고정된 위치로 설정합니다 ---
            zoom=7.0,                           # 한반도가 전체적으로 보이는 줌 레벨
            center={"lat": 36.3, "lon": 127.8}, # 대한민국 중심 좌표
            # ---------------------------------------
            height=650,
            opacity=0.8,
            size="marker_size",
            size_max=15
        )

        # 3. 레이아웃 설정 (bounds 관련 코드 삭제)
        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r":0,"t":0,"l":0,"b":0},
            legend=dict(
                yanchor="top", y=0.99, xanchor="left", x=0.01,
                bgcolor="rgba(255, 255, 255, 0.7)"
            )
        )

        st.plotly_chart(fig, use_container_width=True)
        st.write("") 

        # 4. 휴게소 상세 리스트 (UX/디자인 대폭 개선)
        st.markdown(f"### 📋 노선별 상세 휴게소 현황")
        st.info("선택하신 노선별로 휴게소 명단을 확인하실 수 있습니다.")

        # 노선별로 섹션을 나누어 표시
        # 선택된 노선이 많을 경우 페이지가 너무 길어지지 않게 루프를 돌며 Expander 혹은 Tabs를 활용합니다.
        
        if len(selected_routes) > 1:
            # 여러 노선이 선택된 경우: Tabs를 사용하여 깔끔하게 분리 (UX 권장)
            tabs = st.tabs([f"🛣️ {route}" for route in selected_routes])
            
            for i, route in enumerate(selected_routes):
                with tabs[i]:
                    route_df = filtered_df[filtered_df['route_name'] == route]
                    st.markdown(f"**{route}**에는 총 **{len(route_df)}개**의 휴게소가 있습니다.")
                    
                    # 불필요한 정보 제거 후 명칭만 노출
                    display_df = route_df[['restarea_name']].rename(columns={'restarea_name': '휴게소 명칭'})
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        else:
            # 단일 노선만 선택된 경우: 바로 리스트 노출
            route = selected_routes[0]
            route_df = filtered_df[filtered_df['route_name'] == route]
            
            with st.container():
                st.markdown(f"#### 📍 {route} 휴게소 명단")
                # 디자인적 요소를 위해 단순 표 대신 깔끔한 dataframe 사용
                display_df = route_df[['restarea_name']].rename(columns={'restarea_name': '휴게소 명칭'})
                st.dataframe(display_df, use_container_width=True, hide_index=True)

    else:
        st.info("노선을 선택하면 지도가 표시됩니다.")