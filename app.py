import streamlit as st

# 🌟 분리해 둔 화면 함수들을 불러옵니다!
from page_faq import show_faq
from page_stats import show_stats, show_yearly_stats  # 👈 show_yearly_stats 추가!
from page_traffic import show_page
import page_map  # 새로 만든 지도 페이지 모듈
import page_traffic_time # 👈 새로 만든 실시간 소요시간 페이지 모듈 임포트!
from sidebar import sidebar
from PIL import Image 
import pillow_avif

# 페이지 기본 설정
st.set_page_config(page_title="HI-REST", page_icon="🛣️", layout="wide")

# 👈 메뉴에 '연도별 등록 추이'를 추가했습니다.
menu = sidebar()

if menu == "메인 홈":

    import base64
    import streamlit.components.v1 as components
    
    st.markdown("""
    <style>
    /* 메인 본문 폭/여백 제거 */
    .block-container {
        max-width: 100% !important;
        padding-top: 0rem !important;
        padding-right: 0rem !important;
        padding-left: 0rem !important;
        padding-bottom: 0rem !important;
    }

    /* 상단 툴바 아래쪽 기본 여백도 줄이기 */
    [data-testid="stAppViewContainer"] > .main {
        padding-top: 0rem !important;
    }

    /* components iframe 바깥 여백 제거 */
    [data-testid="stIFrame"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    def img_to_base64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    # 이미지 파일 경로 확인 필요
    img_base64 = img_to_base64("highway.png")

    hero_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            font-family: sans-serif;
        }}

        .hero-wrap {{
            position: relative;
            width: 100%;
            height: 88vh;
            overflow: hidden;
        }}

        .hero-bg {{
            position: absolute;
            inset: 0;
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            filter: brightness(0.78);
        }}

        .hero-overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(
                to right,
                rgba(0,0,0,0.35) 0%,
                rgba(0,0,0,0.18) 35%,
                rgba(0,0,0,0.18) 65%,
                rgba(0,0,0,0.35) 100%
            );
        }}

        .hero-content {{
            position: relative;
            z-index: 2;
            height: 100%;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            align-items: center;
            padding: 0 5vw;
            color: white;
            box-sizing: border-box;
        }}

        .hero-left, .hero-center, .hero-right {{
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .hero-left {{
            align-items: flex-start;
            text-align: left;
        }}

        .hero-center {{
            align-items: center;
            text-align: center;
        }}

        .hero-right {{
            align-items: flex-end;
            text-align: right;
        }}

        .hero-line {{
            width: 80px;
            height: 4px;
            background: rgba(255,255,255,0.85);
            margin-bottom: 22px;
            border-radius: 999px;
        }}

        .hero-title {{
            font-size: clamp(2rem, 4vw, 4rem);
            font-weight: 800;
            line-height: 1.2;
            margin: 0;
        }}

        /* 👇 여기서부터 수정된 부분입니다 (글자 크기, 두께, 자간 조정) */
        .hero-label {{
            font-size: clamp(3rem, 6vw, 6rem); /* 양옆 글자보다 살짝 더 크게 설정 */
            font-weight: 900;                  /* 가장 굵은 폰트 적용 */
            line-height: 1.2;
            margin: 0;
            letter-spacing: 4px;               /* 글자 간격을 넓혀서 로고 느낌 강조 */
            text-shadow: 2px 2px 10px rgba(0,0,0,0.3); /* 배경에 묻히지 않게 은은한 그림자 추가 */
        }}
        /* 👆 수정 끝 */

        .hero-number {{
            font-size: clamp(4rem, 10vw, 7.5rem);
            font-weight: 900;
            line-height: 1;
            margin: 0;
        }}

        .hero-unit {{
            font-size: 1.8rem;
            font-weight: 700;
            margin-top: 10px;
            opacity: 0.9;
        }}

        .hero-bottom-bar {{
            position: absolute;
            left: 50%;
            bottom: 28px;
            transform: translateX(-50%);
            width: 180px;
            height: 8px;
            background: rgba(255,255,255,0.25);
            border-radius: 999px;
            overflow: hidden;
            z-index: 3;
        }}

        .hero-bottom-bar-fill {{
            width: 42%;
            height: 100%;
            background: #1d9bf0;
            border-radius: 999px;
        }}
    </style>
    </head>
    <body>
        <div class="hero-wrap">
            <div class="hero-bg"></div>
            <div class="hero-overlay"></div>

            <div class="hero-content">
                <div class="hero-left">
                    <div class="hero-line"></div>
                    <h1 class="hero-title">차량 흐름과<br>도로 이용 현황</h1>
                </div>

                <div class="hero-center">
                    <div class="hero-label">HI-REST</div>
                </div>

                <div class="hero-right">
                    <div class="hero-line"></div>
                    <h1 class="hero-title">다양한 휴게소 <br>정보 제공</h1>
                </div>
            </div>

            <div class="hero-bottom-bar">
                <div class="hero-bottom-bar-fill"></div>
            </div>
        </div>
    </body>
    </html>
    """

    components.html(hero_html, height=800, scrolling=False)

elif menu == "등록된 자동차 통계":
    show_stats() # 기존 carmaster_db 데이터 화면

elif menu == "연도별 등록 추이":
    show_yearly_stats() # 👈 신규 vehicle_db_year 데이터 화면

elif menu == "연도별 고속도로 통행량":  # 👈 사용자가 이 메뉴를 클릭하면
    show_page()

elif menu == "주요 지역 소요 시간": # 👈 신규 추가된 메뉴 연결!
    page_traffic_time.show_page()
    
elif menu == "휴게소 정보":
    pass
    
elif menu == "FAQ 게시판":
    show_faq() 

elif menu == "휴게소 위치 지도":
    # 새로 만든 page_map.py 안의 함수를 호출!
    page_map.show_rest_area_map()