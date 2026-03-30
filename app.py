import streamlit as st

# 🌟 분리해 둔 화면 함수들을 불러옵니다!
from page_faq import show_faq
from page_stats import show_stats, show_yearly_stats  # 👈 show_yearly_stats 추가!

# 페이지 기본 설정
st.set_page_config(page_title="통합 플랫폼 대시보드", page_icon="🚥", layout="wide")

# 사이드바 (메뉴 이동)
st.sidebar.title("🚥 메뉴 이동")

# 👈 메뉴에 '연도별 등록 추이'를 추가했습니다.
menu = st.sidebar.radio("원하시는 메뉴를 선택하세요", [
    "🏠 메인 홈", 
    "❓ FAQ 게시판", 
    "📊 맞춤형 자동차 통계", 
    "📈 연도별 등록 추이"
])
st.sidebar.markdown("---")

# 메인 화면 로직 분기
if menu == "🏠 메인 홈":
    st.title("환영합니다! 👋")
    st.write("통합 플랫폼의 메인 화면입니다. 왼쪽 사이드바에서 원하시는 메뉴를 선택해 주세요!")

elif menu == "❓ FAQ 게시판":
    show_faq() 

elif menu == "📊 맞춤형 자동차 통계":
    show_stats() # 기존 carmaster_db 데이터 화면

elif menu == "📈 연도별 등록 추이":
    show_yearly_stats() # 👈 신규 vehicle_db_year 데이터 화면