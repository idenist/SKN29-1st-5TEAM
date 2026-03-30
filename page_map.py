import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# --- .env 로드 및 설정 ---
load_dotenv()
DB_HOST = os.getenv("DB_HOST", "127.0.0.1").strip()
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
    # image_6e149a.png의 컬럼명 기준
    query = "SELECT restarea_name, route_name, xValue, yValue, service_area_code FROM rest_areas"
    try:
        return pd.read_sql_query(query, _engine)
    except Exception as e:
        st.error(f"⚠️ rest_areas 테이블 로드 오류: {e}")
        return pd.DataFrame()

# ==========================================
# 1. 상세 데이터 조회 (테이블명 에러 수정 반영)
# ==========================================
def fetch_restarea_details(_engine, restarea_name):
    # 주유소 검색용 이름 변환
    gas_station_name = restarea_name.replace("휴게소", "주유소")

    try:
        # 음식 정보 (foodinfo)
        df_food = pd.read_sql(f"SELECT foodNm, foodCost, bestfoodyn, etc FROM foodinfo WHERE restarea_name = '{restarea_name}'", _engine)
    except:
        df_food = pd.DataFrame()

    try:
        # 주유소 정보 (에러 발생했던 부분: rest_areas_gas -> rest_area_gas로 수정 시도)
        # 만약 여전히 에러가 난다면 DB의 실제 테이블명을 확인해주세요.
        query_gas = f"SELECT gasoline_price, disel_price, lpg_price, lpgYn, svarAddr FROM rest_area_gas WHERE restarea_name = '{gas_station_name}'"
        df_gas = pd.read_sql(query_gas, _engine)
        gas_info = df_gas.iloc[0] if not df_gas.empty else None
    except Exception as e:
        # 주유소 테이블 조회 실패 시 안내 (DB에 테이블 이름 확인 필요)
        st.warning(f"⚠️ 주유소 정보 조회 불가 (테이블명을 확인해주세요): {e}")
        gas_info = None

    try:
        # 이벤트 정보 (rest_area_events)
        df_events = pd.read_sql(f"SELECT event_name, event_detail, start_time, end_time FROM rest_area_events WHERE restarea_name = '{restarea_name}'", _engine)
    except:
        df_events = pd.DataFrame()

    return df_food, gas_info, df_events

# ==========================================
# 2. 팝업창 (Dialog) UI
# ==========================================
@st.dialog("휴게소 상세 정보", width="large")
def show_detail_popup(_engine, restarea_name):
    st.header(f"🏛️ {restarea_name}")
    
    df_food, gas_info, df_events = fetch_restarea_details(_engine, restarea_name)

    # --- 주유소 정보 ---
    st.subheader("⛽ 주유소 및 충전소 정보")
    if gas_info is not None:
        if pd.notna(gas_info.get('svarAddr')):
            st.info(f"📍 주소: {gas_info['svarAddr']}")

        g1, g2, g3 = st.columns(3)
        gas_p = f"{int(gas_info['gasoline_price']):,}원" if pd.notna(gas_info['gasoline_price']) else "정보 없음"
        disel_p = f"{int(gas_info['disel_price']):,}원" if pd.notna(gas_info['disel_price']) else "정보 없음"
        
        g1.metric("휘발유", gas_p)
        g2.metric("경유", disel_p)
        
        if str(gas_info.get('lpgYn')) == '1':
            lpg_p = f"{int(gas_info['lpg_price']):,}원" if pd.notna(gas_info['lpg_price']) else "가격 미정"
            g3.metric("LPG", lpg_p)
        else:
            g3.metric("LPG", "미운영")
    else:
        st.write("등록된 주유소 정보가 없습니다.")

    st.divider()

    # --- 음식 정보 ---
    st.subheader("🍴 대표 메뉴 및 식당가")
    if not df_food.empty:
        df_food.fillna({'foodNm': '메뉴명 없음', 'foodCost': 0, 'etc': ''}, inplace=True)
        df_food.columns = ['메뉴명', '가격', '베스트', '설명']
        st.dataframe(df_food, use_container_width=True, hide_index=True)
    else:
        st.write("식당가 정보가 등록되지 않았습니다.")

    if st.button("닫기"):
        st.rerun()

# ==========================================
# 3. 메인 지도 및 리스트 서비스
# ==========================================
def show_rest_area_map():
    st.title("📍 고속도로 휴게소 탐색기")
    
    engine = get_rest_area_db_connection()
    if not engine: return

    df = load_all_rest_areas(engine)
    if df.empty: return

    # 필터
    all_routes = sorted(df['route_name'].unique().tolist())
    selected_routes = st.multiselect("🗺️ 노선 선택", options=all_routes, default=['경부선'] if '경부선' in all_routes else [all_routes[0]])
    filtered_df = df[df['route_name'].isin(selected_routes)].copy()

    # 지도 시각화
    fig = px.scatter_mapbox(
        filtered_df, lat="yValue", lon="xValue", hover_name="restarea_name",
        color="route_name", zoom=7, center={"lat": 36.3, "lon": 127.8},
        height=500, mapbox_style="open-street-map"
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

    # 상세 리스트 (클릭 시 바로 팝업)
    st.subheader("📋 휴게소 명단")
    st.caption("목록의 행을 클릭하면 상세 정보 팝업이 나타납니다.")

    if not filtered_df.empty:
        # 화면에 보여줄 명칭만 추출
        list_df = filtered_df[['restarea_name']].rename(columns={'restarea_name': '휴게소 이름'})
        
        # selection_mode="single-row"와 on_select="rerun"을 조합하여 
        # 체크박스 클릭이 아닌 '행 클릭' 시 바로 작동하게 함
        selected_data = st.dataframe(
            list_df,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row"
        )

        # 행 선택(클릭) 이벤트 발생 시
        if len(selected_data.selection.rows) > 0:
            idx = selected_data.selection.rows[0]
            selected_name = list_df.iloc[idx]['휴게소 이름']
            show_detail_popup(engine, selected_name)

if __name__ == '__main__':
    show_rest_area_map()