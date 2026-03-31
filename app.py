import streamlit as st
import base64
import streamlit.components.v1 as components

# 각 페이지 모듈 임포트 (기존 경로 유지)
from page_faq import show_faq
from page_stats import show_stats, show_yearly_stats 
from page_traffic import show_page
import page_map  
import page_traffic_time 
from sidebar import sidebar

# 1. 페이지 기본 설정
st.set_page_config(page_title="HI-REST", page_icon="🛣️", layout="wide")

# 2. [전역 설정] 모든 페이지 상단 헤더 색상 고정 (멜란지 그레이)
st.markdown("""
    <style>
    header[data-testid="stHeader"] {
        background-color: #E9ECEF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 사이드바에서 메뉴 선택 결과 가져오기
menu = sidebar()

# 3. 메뉴별 여백 및 콘텐츠 설정
if menu == "메인 홈":
    # [메인 홈 전용 CSS] 배경 이미지가 상단에 딱 붙도록 여백 제거
    st.markdown("""
        <style>
        .block-container {
            max-width: 100% !important;
            padding-top: 0rem !important;
            padding-right: 0rem !important;
            padding-left: 0rem !important;
            padding-bottom: 0rem !important;
        }
        [data-testid="stAppViewContainer"] > .main {
            padding-top: 0rem !important;
        }
        [data-testid="stIFrame"] {
            margin: 0 !important;
            padding: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    def img_to_base64(path):
        try:
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except FileNotFoundError:
            return ""

    # 이미지 파일 로드
    img_base64 = img_to_base64("highway.png")

    hero_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; font-family: sans-serif; }}
        .hero-wrap {{ position: relative; width: 100%; height: 88vh; overflow: hidden; }}
        .hero-bg {{ 
            position: absolute; inset: 0; 
            background-image: url("data:image/png;base64,{img_base64}"); 
            background-size: cover; background-position: center; background-repeat: no-repeat; 
            filter: brightness(0.78);
        }}
        .hero-overlay {{
            position: absolute; inset: 0;
            background: linear-gradient(to right, rgba(0,0,0,0.35) 0%, rgba(0,0,0,0.18) 35%, rgba(0,0,0,0.18) 65%, rgba(0,0,0,0.35) 100%);
        }}
        .hero-content {{
            position: relative; z-index: 2; height: 100%; display: grid;
            grid-template-columns: 1fr 1fr 1fr; align-items: center; padding: 0 5vw; color: white; box-sizing: border-box;
        }}
        .hero-left, .hero-center, .hero-right {{ display: flex; flex-direction: column; justify-content: center; }}
        .hero-left {{ align-items: flex-start; text-align: left; }}
        .hero-center {{ align-items: center; text-align: center; width:550px; }}
        .hero-right {{ align-items: flex-end; text-align: right; }}
        .hero-line {{ width: 80px; height: 4px; background: rgba(255,255,255,0.85); margin-bottom: 22px; border-radius: 999px; }}
        .hero-title {{ font-size: clamp(2rem, 4vw, 2rem); font-weight: 800; line-height: 1.2; margin: 0; }}
        .hero-label {{ font-size: clamp(2rem, 6vw, 2rem); font-weight: 900; line-height: 1.2; margin: 0; letter-spacing: 4px; text-shadow: 2px 2px 10px rgba(0,0,0,0.3); }}
        .hero-brand {{ font-family: "Coral Black", "Impact", sans-serif; font-size: clamp(8rem, 8vw, 8rem); font-weight: 900; text-transform: uppercase; color: white; line-height: 1; text-shadow: 0 4px 12px rgba(0,0,0,0.35), 0 1px 0 rgba(255,255,255,0.15); }}
        .hero-unit {{ font-size: 1.3rem; font-weight: 700; margin-top: 10px; opacity: 0.9; }}
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
                    <div class="hero-label">SKN 29th</div>
                    <div class="hero-brand">HI REST</div>
                    <div class="hero-unit">Drive Smart, Rest Better</div>
                </div>
                <div class="hero-right">
                    <div class="hero-line"></div>
                    <h1 class="hero-title">다양한 휴게소 <br>정보 제공</h1>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(hero_html, height=800, scrolling=False)

else:
    # [일반 페이지 공통 CSS] 제목이 회색 헤더에 가려지지 않도록 상단 여백 추가
    st.markdown("""
        <style>
        .block-container {
            padding-top: 5rem !important;
            padding-bottom: 2rem !important;
        }
        </style>
        """, unsafe_allow_html=True)

    if menu == "등록된 자동차 통계":
        show_stats()

    elif menu == "연도별 등록 추이":
        show_yearly_stats()

    elif menu == "연도별 고속도로 통행량":
        show_page()

    elif menu == "주요 지역 소요 시간":
        page_traffic_time.show_page()
        
    elif menu == "휴게소 정보":
        pass
        
    elif menu == "FAQ 게시판":
        show_faq() 

    elif menu == "휴게소 위치 지도":
        page_map.show_rest_area_map()