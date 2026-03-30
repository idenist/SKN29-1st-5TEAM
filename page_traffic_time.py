import streamlit as st
import pymysql
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 가장 최근 데이터 1줄 가져오기
def get_latest_traffic_data():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME_TRAFFIC"), # 환경변수 이름 확인
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # id를 기준으로 내림차순 정렬하여 가장 최근 1개 데이터만 가져옴
            sql = "SELECT * FROM forecast_traffic ORDER BY id DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        st.error(f"데이터베이스 연결 오류가 발생했습니다: {e}")
        return None
# 주요 도시
def show_page():
    st.title("⏱️ 주요 도시 소요시간")
    
    data = get_latest_traffic_data()
    if not data:
        st.warning("현재 소요시간 데이터를 불러올 수 없습니다.")
        return
    
    # 상단 기준 시간 표시 포맷팅
    sdate = str(data['sdate'])
    stime = str(data['stime'])
    
    # 데이터 형태에 따른 안전한 포맷팅 처리
    if len(sdate) == 8 and len(stime) >= 4:
        formatted_date = f"{sdate[:4]}.{sdate[4:6]}.{sdate[6:]} {stime[:2]}:{stime[2:4]}"
    else:
        formatted_date = f"{sdate} {stime}"

    # 1. 기준 시간 크기 키우기 (HTML h3 태그 적용) & 3. 구분선(---) 제거
    st.markdown(f"<h3 style='color: #333; margin-bottom: 20px;'>기준 시간: {formatted_date}</h3>", unsafe_allow_html=True)

    # 2. 기타 노선을 위한 탭 3개로 확장
    tab1, tab2, tab3 = st.tabs(["🛣️ 서울 출발 (하행)", "🛣️ 서울 도착 (상행)", "🛣️ 기타 노선"])

    # Streamlit에 CSS를 주입하여 카드 형태 디자인 적용
    st.markdown("""
        <style>
        .city-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            text-align: center;
            border: 1px solid #e0e0e0;
            border-top: 5px solid #08c7b4; /* 사이드바 포인트 컬러와 맞춤 */
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
        """'3:40' 형태의 문자열을 '3시간 40분'으로 변환"""
        if time_str and ":" in str(time_str):
            parts = str(time_str).split(":")
            if len(parts) >= 2:
                # 0시간인 경우 처리 등 세밀한 조정 가능
                if parts[0] == "0":
                    return f"{parts[1]}분"
                return f"{parts[0]}시간 {parts[1]}분"
        return time_str if time_str else "-"

    def render_cards(routes_dict):
        """딕셔너리를 받아 3열 카드로 렌더링"""
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

    # --- 탭 1: 서울 출발 ---
    with tab1:
        st.subheader("서울에서 출발하는 노선")
        st.write("") # 여백
        routes_from_seoul = {
            "서울 ➔ 부산": data.get("csubs", "-"),
            "서울 ➔ 대구": data.get("csudg", "-"),
            "서울 ➔ 대전": data.get("csudj", "-"),
            "서울 ➔ 광주": data.get("csugj", "-"),
            "서울 ➔ 강릉": data.get("csukr", "-"),
            "서울 ➔ 목포": data.get("csump", "-"),
            "서울 ➔ 울산": data.get("csuus", "-")
            # 남양주->양양 제거
        }
        render_cards(routes_from_seoul)

    # --- 탭 2: 서울 도착 ---
    with tab2:
        st.subheader("서울로 도착하는 노선")
        st.write("") # 여백
        routes_to_seoul = {
            "부산 ➔ 서울": data.get("cbssu", "-"),
            "대구 ➔ 서울": data.get("cdgsu", "-"),
            "대전 ➔ 서울": data.get("cdjsu", "-"),
            "광주 ➔ 서울": data.get("cgjsu", "-"),
            "강릉 ➔ 서울": data.get("ckrsu", "-"),
            "목포 ➔ 서울": data.get("cmpsu", "-"),
            "울산 ➔ 서울": data.get("cussu", "-")
            # 양양->남양주 제거
        }
        render_cards(routes_to_seoul)

    # --- 탭 3: 기타 노선 ---
    with tab3:
        st.subheader("기타 노선 (수도권 ↔ 강원)")
        st.write("") # 여백
        routes_other = {
            "남양주 ➔ 양양": data.get("csuyy", "-"),
            "양양 ➔ 남양주": data.get("cyysu", "-")
        }
        render_cards(routes_other)