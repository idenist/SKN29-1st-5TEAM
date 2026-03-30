import streamlit as st
from sidebar import sidebar
import main_page
import current_situation
import rest_place

st.set_page_config(
    page_title="전국자동차등록 현황 및 기업 FAQ 조회 시스템",
    layout="wide"  # 화면을 넓게 사용 (기본값은 "centered")
)

# ============================================
# 사이드바에서 선택한 메뉴 항목에 따라 다른 화면을 보여줌
# ============================================
menu = sidebar()

if menu == "메인 페이지":
    main_page.main()
elif menu == "연간 현황 정보":
    current_situation.main()
elif menu == "휴게소 정보":
    rest_place.main()