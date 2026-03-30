import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.engine import URL  # 👈 URL 조립 도구 추가
import pymysql
import os
from dotenv import load_dotenv

# --- .env 파일 로드 ---
load_dotenv()

# ==============================================================================
# 환경 변수에서 DB 접속 정보 가져오기
# .strip()을 사용하여 혹시 모를 앞뒤 공백이나 줄바꿈 문자를 제거합니다.
# ==============================================================================
DB_HOST = os.getenv("DB_HOST", "127.0.0.1").strip().replace("@", "") # @ 기호 강제 제거
DB_PORT = os.getenv("DB_PORT", "3306").strip()
DB_USER = os.getenv("DB_USER", "root").strip()
DB_PWD  = os.getenv("DB_PASSWORD", "").strip()
DB_NAME_REST = os.getenv("DB_NAME_REST", "rest_area").strip() # DB 이름

@st.cache_resource
def get_rest_area_db_connection():
    try:
        # 1. 환경 변수 청소 (앞뒤 공백 및 불필요한 @ 제거)
        host = DB_HOST.strip().replace("@", "")
        user = DB_USER.strip()
        pwd  = DB_PWD.strip()
        port = int(DB_PORT.strip()) # 포트는 숫자로 변환
        db   = DB_NAME_REST.strip()

        # 2. [핵심] URL 객체 사용 (f-string 방식의 @ 오류를 원천 차단)
        connection_url = URL.create(
            drivername="mysql+pymysql",
            username=user,
            password=pwd,
            host=host,
            port=port,
            database=db,
            query={"charset": "utf8mb4"}
        )
        
        # 3. 엔진 생성
        engine = create_engine(connection_url, connect_args={'connect_timeout': 10})
        return engine

    except Exception as e:
        st.error(f"⚠️ 휴게소 DB 연결 실패: {e}")
        return None

@st.cache_data
def load_all_rest_areas(_engine):
    if _engine is None:
        return pd.DataFrame()
    
    # 테이블 이름은 이미지에 나온 대로 'rest_areas' (복수형)를 사용합니다.
    query = "SELECT restarea_name, route_name, xValue, yValue, service_area_code FROM rest_areas"
    
    try:
        df = pd.read_sql_query(query, _engine)
        return df
    except Exception as e:
        # 테이블 이름이 틀렸을 경우를 위해 에러 메시지 상세 출력
        st.error(f"⚠️ 데이터를 가져오는 중 오류 발생: {e}")
        return pd.DataFrame()

# ==========================================
# 메인 화면에 그릴 함수 정의
# ==========================================
def show_rest_area_map():
    st.title("🛰️ 전국 고속도로 휴게소 노선별 지도")
    st.markdown("DB 데이터를 실시간으로 불러오며, 왼쪽 사이드바에서 노선별로 필터링할 수 있습니다.")
    st.markdown("---")

    engine = get_rest_area_db_connection()

    if engine:
        with st.spinner('DB에서 휴게소 정보를 불러오는 중...'):
            df = load_all_rest_areas(engine)

        if not df.empty:
            # 사이드바 필터링
            st.sidebar.header("🔍 노선 필터링")
            all_routes = sorted(df['route_name'].unique().tolist())
            selected_routes = st.sidebar.multiselect(
                "조회할 노선을 선택하세요", 
                options=all_routes, 
                default=all_routes
            )
            
            filtered_df = df[df['route_name'].isin(selected_routes)]

            if filtered_df.empty:
                st.warning("선택한 노선에 해당하는 휴게소가 없습니다.")
            else:
                st.success(f"✅ 현재 **{len(selected_routes)}개 노선**, 총 **{len(filtered_df):,}개**의 휴게소를 표시 중입니다.")

                # Plotly 지도 시각화
                fig = px.scatter_mapbox(
                    filtered_df,
                    lat="yValue",
                    lon="xValue",
                    hover_name="restarea_name",
                    hover_data={"route_name": True, "service_area_code": True, "yValue": False, "xValue": False},
                    color="route_name",
                    zoom=6.5,
                    center={"lat": 36.5, "lon": 127.8},
                    height=750,
                    opacity=0.8
                )

                fig.update_layout(mapbox_style="open-street-map")
                fig.update_layout(
                    margin={"r":0,"t":0,"l":0,"b":0},
                    legend_title_text='노선명 (클릭하여 켜기/끄기)' 
                ) 

                st.plotly_chart(fig, use_container_width=True)

                with st.expander("필터링된 원본 데이터 테이블 보기"):
                    st.dataframe(filtered_df)
                
        else:
            st.warning("DB 연결은 성공했으나 데이터를 가져오지 못했습니다. 테이블 이름이나 컬럼명을 확인해 주세요.")
    else:
        st.error("DB 접속 정보가 올바르지 않습니다. .env 파일의 DB_HOST 설정을 확인해 주세요.")