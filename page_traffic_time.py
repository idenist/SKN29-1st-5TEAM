import streamlit as st
import pymysql
import os
import requests
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# ==========================================
# 1. DB에서 가장 최근 데이터 가져오기
# ==========================================
def get_latest_traffic_data():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME_TRAFFIC"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            sql = "SELECT * FROM forecast_traffic ORDER BY id DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        st.error(f"데이터베이스 연결 오류가 발생했습니다: {e}")
        return None

# ==========================================
# 2. ITS API로 구간별 대표 CCTV 가져오기 (수정된 좌표 범위)
# ==========================================
def get_route_cctv_url(route_name):
    api_key = os.getenv("ITS_API_KEY")
    if not api_key:
        return None, None

    # 각 노선별 대표 핵심 길목 (검색 성공률을 높이기 위해 범위를 최적화함)
    route_coords = {
        "서울 ➔ 부산": {"minX": 127.10, "maxX": 127.20, "minY": 36.75, "maxY": 36.85}, 
        "부산 ➔ 서울": {"minX": 127.00, "maxX": 127.10, "minY": 37.40, "maxY": 37.50}, 
        "서울 ➔ 대구": {"minX": 127.55, "maxX": 127.65, "minY": 37.20, "maxY": 37.30}, 
        "대구 ➔ 서울": {"minX": 128.10, "maxX": 128.25, "minY": 36.10, "maxY": 36.20}, 
        "서울 ➔ 대전": {"minX": 127.10, "maxX": 127.20, "minY": 37.00, "maxY": 37.10}, 
        "대전 ➔ 서울": {"minX": 127.35, "maxX": 127.45, "minY": 36.40, "maxY": 36.50}, 
        "서울 ➔ 광주": {"minX": 127.05, "maxX": 127.18, "minY": 36.10, "maxY": 36.25}, 
        "광주 ➔ 서울": {"minX": 127.05, "maxX": 127.15, "minY": 36.55, "maxY": 36.65}, 
        "서울 ➔ 강릉": {"minX": 127.30, "maxX": 127.45, "minY": 37.15, "maxY": 37.30}, 
        "강릉 ➔ 서울": {"minX": 128.60, "maxX": 128.80, "minY": 37.60, "maxY": 37.75}, 
        "서울 ➔ 목포": {"minX": 126.80, "maxX": 126.90, "minY": 36.90, "maxY": 37.00}, 
        "목포 ➔ 서울": {"minX": 126.75, "maxX": 126.85, "minY": 36.85, "maxY": 36.95}, 
        "서울 ➔ 울산": {"minX": 128.90, "maxX": 129.05, "minY": 35.90, "maxY": 36.00}, 
        "울산 ➔ 서울": {"minX": 129.10, "maxX": 129.25, "minY": 35.50, "maxY": 35.60}, 
        "남양주 ➔ 양양": {"minX": 127.40, "maxX": 127.55, "minY": 37.60, "maxY": 37.75}, 
        "양양 ➔ 남양주": {"minX": 128.10, "maxX": 128.30, "minY": 37.75, "maxY": 37.95}, 
        "default": {"minX": 127.05, "maxX": 127.15, "minY": 37.30, "maxY": 37.40} 
    }

    matched_coords = None
    for key in route_coords.keys():
        if key in route_name:
            matched_coords = route_coords[key]
            break
            
    if not matched_coords:
        matched_coords = route_coords["default"]

    url = "https://openapi.its.go.kr:9443/cctvInfo"
    params = {
        "apiKey": api_key,
        "type": "ex",          
        "cctvType": "5",       # mp4 동영상
        "minX": matched_coords["minX"], "maxX": matched_coords["maxX"],
        "minY": matched_coords["minY"], "maxY": matched_coords["maxY"],
        "getType": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "response" in data and data["response"]["data"]:
                cctv_info = data["response"]["data"][0]
                return cctv_info["cctvurl"], cctv_info["cctvname"]
    except Exception as e:
        print("API 연동 에러:", e)
    
    return None, None

# ==========================================
# 3. 팝업창(모달) 띄우기 함수 (크기 확대 버전)
# ==========================================
@st.dialog("📺 실시간 CCTV 영상 보기", width="large")
def open_cctv_popup(route_name):
    st.subheader(f"📍 {route_name} 구간 상황")
    
    with st.spinner("영상을 불러오는 중입니다..."):
        cctv_url, cctv_name = get_route_cctv_url(route_name)
        
    if cctv_url:
        st.info(f"**현재 위치:** {cctv_name}")
        
        # 🌟 여기를 수정합니다! autoplay와 muted 옵션을 추가하세요.
        st.video(cctv_url, autoplay=True, muted=True) 
        
    else:
        st.error("해당 구간의 실시간 영상을 불러오지 못했습니다.")
        
    st.write("")
    if st.button("창 닫기", use_container_width=True, type="primary"):
        st.rerun()
# ==========================================
# 4. 화면 UI 구성
# ==========================================
def show_page():
    st.title("⏱️ 주요 도시 소요시간")
    
    data = get_latest_traffic_data()
    
    if not data:
        st.warning("현재 소요시간 데이터를 불러올 수 없습니다.")
        return
    
    sdate = str(data['sdate'])
    stime = str(data['stime'])
    
    if len(sdate) == 8 and len(stime) >= 4:
        formatted_date = f"{sdate[:4]}.{sdate[4:6]}.{sdate[6:]} {stime[:2]}:{stime[2:4]}"
    else:
        formatted_date = f"{sdate} {stime}"

    st.markdown(f"<h3 style='color: #333; margin-bottom: 20px;'>기준 시간: {formatted_date}</h3>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🛣️ 서울 출발 (하행)", "🛣️ 서울 도착 (상행)", "🛣️ 기타 노선"])

    # 카드 스타일 정의
    st.markdown("""
        <style>
        .city-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 5px; 
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            text-align: center;
            border: 1px solid #e0e0e0;
            border-top: 5px solid #08c7b4; 
        }
        .city-route {
            font-size: 18px;
            color: #444;
            margin-bottom: 15px;
            font-weight: 700;
        }
        .time-value {
            font-size: 28px;
            font-weight: bold;
            color: #005A8D;
        }
        </style>
    """, unsafe_allow_html=True)

    def format_time(time_str):
        if time_str and ":" in str(time_str):
            parts = str(time_str).split(":")
            if len(parts) >= 2:
                if parts[0] == "0":
                    return f"{parts[1]}분"
                return f"{parts[0]}시간 {parts[1]}분"
        return time_str if time_str else "-"

    def render_cards(routes_dict):
        cols = st.columns(3)
        for i, (route_name, time_str) in enumerate(routes_dict.items()):
            formatted_time = format_time(time_str)
            with cols[i % 3]:
                st.markdown(f"""
                    <div class="city-card">
                        <div class="city-route">{route_name}</div>
                        <div class="time-value">{formatted_time}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # 버튼을 누르면 커진 팝업이 뜹니다!
                if st.button(f"🎥 CCTV 보기", key=f"btn_{route_name}", use_container_width=True):
                    open_cctv_popup(route_name)

    # --- 탭별 렌더링 ---
    with tab1:
        st.subheader("서울에서 출발하는 노선")
        st.write("") 
        routes_from_seoul = {
            "서울 ➔ 부산": data.get("csubs", "-"), "서울 ➔ 대구": data.get("csudg", "-"),
            "서울 ➔ 대전": data.get("csudj", "-"), "서울 ➔ 광주": data.get("csugj", "-"),
            "서울 ➔ 강릉": data.get("csukr", "-"), "서울 ➔ 목포": data.get("csump", "-"),
            "서울 ➔ 울산": data.get("csuus", "-")
        }
        render_cards(routes_from_seoul)

    with tab2:
        st.subheader("서울로 도착하는 노선")
        st.write("") 
        routes_to_seoul = {
            "부산 ➔ 서울": data.get("cbssu", "-"), "대구 ➔ 서울": data.get("cdgsu", "-"),
            "대전 ➔ 서울": data.get("cdjsu", "-"), "광주 ➔ 서울": data.get("cgjsu", "-"),
            "강릉 ➔ 서울": data.get("ckrsu", "-"), "목포 ➔ 서울": data.get("cmpsu", "-"),
            "울산 ➔ 서울": data.get("cussu", "-")
        }
        render_cards(routes_to_seoul)

    with tab3:
        st.subheader("기타 노선 (수도권 ↔ 강원)")
        st.write("") 
        routes_other = {
            "남양주 ➔ 양양": data.get("csuyy", "-"), "양양 ➔ 남양주": data.get("cyysu", "-")
        }
        render_cards(routes_other)