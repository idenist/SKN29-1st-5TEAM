import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
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
    query = "SELECT restarea_name, route_name, xValue, yValue, service_area_code FROM rest_areas"
    try:
        return pd.read_sql_query(query, _engine)
    except Exception as e:
        st.error(f"⚠️ 데이터 로드 오류: {e}")
        return pd.DataFrame()

def fetch_restarea_details(_engine, restarea_name):
    gas_station_name = restarea_name.replace("휴게소", "주유소")
    try:
        df_food = pd.read_sql(f"SELECT foodNm, foodCost, bestfoodyn, etc FROM foodinfo WHERE restarea_name = '{restarea_name}'", _engine)
    except:
        df_food = pd.DataFrame()

    try:
        query_gas = f"SELECT gasoline_price, disel_price, lpg_price, lpgYn, svarAddr FROM rest_area_gas WHERE restarea_name = '{gas_station_name}'"
        df_gas = pd.read_sql(query_gas, _engine)
        gas_info = df_gas.iloc[0] if not df_gas.empty else None
    except:
        gas_info = None

    return df_food, gas_info

# ==========================================
# 1. 팝업창 (Dialog) UI 개선
# ==========================================
@st.dialog("상세 정보", width="large")
def show_detail_popup(_engine, restarea_name):
    df_food, gas_info = fetch_restarea_details(_engine, restarea_name)

    # 상단 휴게소 명
    st.header(f"🏛️ {restarea_name}")
    
    # [수정] 주소 디자인: 배경/박스 제거, 검은색 볼드, 제목보다 작은 크기
    if gas_info is not None and pd.notna(gas_info.get('svarAddr')):
        st.markdown(f"<p style='color: black; font-weight: bold; font-size: 1.1rem; margin-top: -10px;'>📍 주소: {gas_info['svarAddr']}</p>", unsafe_allow_html=True)
    st.write("")

    # 주유소 정보
    st.subheader("⛽ 주유소 및 충전소 정보")
    if gas_info is not None:
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

    # 식당 정보
    st.subheader("🍴 대표 메뉴 및 식당가")
    if not df_food.empty:
        df_food.fillna({'foodNm': '메뉴명 없음', 'foodCost': 0, 'etc': '', 'bestfoodyn': 'N'}, inplace=True)
        
        # 베스트 메뉴 추출
        best_menus = df_food[df_food['bestfoodyn'] == 'Y']['foodNm'].tolist()
        if best_menus:
            st.markdown(f"⭐ **베스트 메뉴**: {', '.join([f'**{m}**' for m in best_menus])}")
            st.write("")

        # 메뉴판 테이블 (베스트 컬럼 제외)
        display_food = df_food[['foodNm', 'foodCost', 'etc']].copy()
        display_food.columns = ['메뉴명', '가격', '설명']
        
        st.dataframe(
            display_food, 
            use_container_width=True, 
            hide_index=True,
            column_config={"가격": st.column_config.NumberColumn(format="%d원")}
        )
    else:
        st.write("식당가 정보가 등록되지 않았습니다.")

    st.write("")
    # [기능 확인] 닫기 버튼: 클릭 시 팝업 닫힘
    if st.button("닫기", use_container_width=True):
        st.rerun()

# ==========================================
# 2. 메인 화면
# ==========================================
def show_rest_area_map():
    st.title("📍 고속도로 휴게소 탐색기")
    
    engine = get_rest_area_db_connection()
    if not engine: return

    df = load_all_rest_areas(engine)
    if df.empty: return

    # 노선 필터링
    all_routes = sorted(df['route_name'].unique().tolist())
    selected_routes = st.multiselect("🗺️ 노선 선택", options=all_routes, default=['경부선'] if '경부선' in all_routes else [all_routes[0]])
    filtered_df = df[df['route_name'].isin(selected_routes)].copy()

    # 지도 표시
    fig = px.scatter_mapbox(
        filtered_df, lat="yValue", lon="xValue", hover_name="restarea_name",
        color="route_name", zoom=7, center={"lat": 36.3, "lon": 127.8},
        height=500, mapbox_style="open-street-map"
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

    # [중요 수정] 체크박스 없는 리스트 구현
    st.subheader("📋 휴게소 명단")
    st.info("이름을 클릭하면 상세 정보를 확인할 수 있습니다.")

    if not filtered_df.empty:
        # 데이터프레임 대신 버튼 리스트로 구현하여 "클릭 시 즉시 팝업" 효과 부여
        # 리스트가 너무 길어질 수 있으므로 scrollable container 사용 (선택 사항)
        with st.container(height=400):
            for name in filtered_df['restarea_name']:
                # 각 휴게소 이름을 버튼으로 만들고 클릭 시 팝업 함수 호출
                if st.button(name, use_container_width=True, key=f"btn_{name}"):
                    show_detail_popup(engine, name)

if __name__ == '__main__':
    show_rest_area_map()