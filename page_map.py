import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# 페이지 설정
st.set_page_config(layout="wide", page_title="고속도로 휴게소 탐색기")

# --- .env 로드 ---
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
    # 1. 음식 정보
    try:
        df_food = pd.read_sql(f"SELECT foodNm, foodCost, bestfoodyn, etc FROM rest_area_foods WHERE restarea_name = '{restarea_name}'", _engine)
    except: df_food = pd.DataFrame()
    
    # 2. 주유소 정보
    try:
        query_gas = f"SELECT gasoline_price, disel_price, lpg_price, lpgYn, svarAddr FROM rest_area_gas WHERE restarea_name = '{restarea_name}'"
        df_gas = pd.read_sql(query_gas, _engine)
        gas_info = df_gas.iloc[0] if not df_gas.empty else None
    except: gas_info = None
    
    # 3. 행사 정보
    try:
        query_events = f"SELECT event_name, start_time, end_time, event_detail FROM rest_area_events WHERE restarea_name = '{restarea_name}'"
        df_events = pd.read_sql(query_events, _engine)
    except: df_events = pd.DataFrame()

    # 4. 편의 시설 정보
    try:
        query_amenties = f"SELECT rest_eng, rest_elc, rest_plc, rest_pha, rest_nur FROM rest_area_amenties WHERE restarea_name = '{restarea_name}'"
        df_amenties = pd.read_sql(query_amenties, _engine)
        amenties_info = df_amenties.iloc[0] if not df_amenties.empty else None
    except: amenties_info = None
    
    return df_food, gas_info, df_events, amenties_info

# ==========================================
# 1. 팝업창 (Dialog) UI
# ==========================================
@st.dialog("휴게소 상세 정보", width="large")
def show_detail_popup(_engine, restarea_name):
    df_food, gas_info, df_events, amenties_info = fetch_restarea_details(_engine, restarea_name)

    st.header(f"🏛️ {restarea_name}")
    
    if gas_info is not None and pd.notna(gas_info.get('svarAddr')):
        st.markdown(f"📍 **주소: {gas_info['svarAddr']}**")
    
    # --- 편의 시설 정보 ---
    if amenties_info is not None:
        amenty_list = []
        if amenties_info.get('rest_eng') == 'Y': amenty_list.append("🛠️ 차량정비")
        if amenties_info.get('rest_elc') == 'Y': amenty_list.append("⚡ 전기차충전")
        if amenties_info.get('rest_plc') == 'Y': amenty_list.append("🌳 쉼터")
        if amenties_info.get('rest_pha') == 'Y': amenty_list.append("💊 약국")
        if amenties_info.get('rest_nur') == 'Y': amenty_list.append("🍼 수유실")
        
        if amenty_list:
            st.markdown(f"**보유 시설:** {' | '.join(amenty_list)}")
    
    st.write("")

    # --- 주유소 정보 ---
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
        else: g3.metric("LPG", "미운영")
    else: st.write("등록된 주유소 정보가 없습니다.")

    st.divider()

    # --- 행사 정보 ---
    # 데이터프레임이 비어있지 않은 경우에만 전체 블록을 출력하도록 변경
    if not df_events.empty:
        st.subheader("🎉 진행 중인 행사")
        for _, event in df_events.iterrows():
            with st.expander(f"📌 {event['event_name']} ({event['start_time']} ~ {event['end_time']})", expanded=True):
                clean_detail = str(event['event_detail']).replace('~~', '~')
                st.write(clean_detail)
        st.divider() # 행사가 있을 때만 구분선 표시

    # --- 음식 정보 ---
    st.subheader("🍴 대표 메뉴 및 식당가")
    if not df_food.empty:
        df_food.fillna({'foodNm': '메뉴명 없음', 'foodCost': 0, 'etc': '', 'bestfoodyn': 'N'}, inplace=True)
        best_menus = df_food[df_food['bestfoodyn'] == 'Y']['foodNm'].tolist()
        if best_menus:
            st.markdown(f"⭐ **베스트 메뉴**: {', '.join([f'**{m}**' for m in best_menus])}")
            st.write("")
        
        st.dataframe(
            df_food[['foodNm', 'foodCost', 'etc']].rename(columns={'foodNm': '메뉴명', 'foodCost': '가격', 'etc': '설명'}),
            use_container_width=True,
            hide_index=True,
            column_config={
                "가격": st.column_config.NumberColumn(format="%d원"),
                "설명": st.column_config.TextColumn("설명", width="large")
            }
        )
    else: st.write("식당가 정보가 등록되지 않았습니다.")

    st.write("")
    if st.button("닫기", use_container_width=True, key="btn_close_popup"):
        st.session_state.last_opened = restarea_name 
        st.rerun()

# ==========================================
# 2. 메인 화면
# ==========================================
def show_rest_area_map():
    st.title("🗺️ 노선별 휴게소 정보")
    engine = get_rest_area_db_connection()
    if not engine: return

    if "last_opened" not in st.session_state:
        st.session_state.last_opened = None

    df_all = load_all_rest_areas(engine)
    if df_all.empty: return

    df_all['yValue'] = pd.to_numeric(df_all['yValue'], errors='coerce')
    df_all['xValue'] = pd.to_numeric(df_all['xValue'], errors='coerce')
    df_all = df_all.dropna(subset=['yValue', 'xValue'])

    all_routes = sorted(df_all['route_name'].unique().tolist())
    selected_routes = st.multiselect("🛣️ 노선 선택", options=all_routes, default=['경부선'] if '경부선' in all_routes else [all_routes[0]])
    filtered_df = df_all[df_all['route_name'].isin(selected_routes)].copy()

    if not filtered_df.empty:
        fig = go.Figure()
        routes = filtered_df['route_name'].unique()
        
        # 색상표 가져오기 (Plotly 기본 질적 색상표)
        color_palette = px.colors.qualitative.Plotly

        for i, route in enumerate(routes):
            route_data = filtered_df[filtered_df['route_name'] == route]
            # 노선별로 다른 색상 할당
            marker_color = color_palette[i % len(color_palette)]
            
            fig.add_trace(go.Scattermapbox(
                lat=route_data['yValue'], lon=route_data['xValue'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=18, 
                    color=marker_color,
                    symbol='circle', 
                    opacity=0.9,
                    allowoverlap=True
                ),
                hovertext=route_data['restarea_name'],
                hovertemplate="<b>%{hovertext}</b><br>노선: " + route + "<extra></extra>",
                name=route
            ))

        fig.update_layout(
            mapbox=dict(style="open-street-map", zoom=7.0, center={"lat": 36.3, "lon": 127.8}),
            margin={"r":0,"t":0,"l":0,"b":0}, height=550, uirevision='constant',
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255, 255, 255, 0.7)")
        )

        map_event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="rest_map")

        if "selection" in map_event and map_event.selection and map_event.selection.points:
            clicked_name = map_event.selection.points[0].get('hovertext')
            if clicked_name and clicked_name != st.session_state.last_opened:
                show_detail_popup(engine, clicked_name)
            elif clicked_name is None:
                st.session_state.last_opened = None 
        else:
            st.session_state.last_opened = None

    st.markdown("---")
    
    st.subheader("📋 휴게소 명단")
    search_keyword = st.text_input("🔍 휴게소 검색", placeholder="예: 건천")

    if not filtered_df.empty:
        list_df = filtered_df[filtered_df['restarea_name'].str.contains(search_keyword, case=False, na=False)] if search_keyword else filtered_df

        if list_df.empty:
            st.warning("검색 결과가 없습니다.")
        else:
            # 선택된 노선들 추출 (검색어에 의해 필터링된 결과 기준)
            unique_routes = list_df['route_name'].unique().tolist()
            
            # 노선별 탭(Tab) 생성
            tabs = st.tabs([f"🛣️ {route}" for route in unique_routes])
            
            # 각 탭 내부에 스크롤 영역과 휴게소 버튼 배치
            for i, route in enumerate(unique_routes):
                with tabs[i]:
                    with st.container(height=350):
                        route_df = list_df[list_df['route_name'] == route]
                        
                        for name in route_df['restarea_name']:
                            if st.button(name, use_container_width=True, key=f"btn_list_{route}_{name}"):
                                st.session_state.last_opened = None 
                                show_detail_popup(engine, name)

if __name__ == '__main__':
    show_rest_area_map()