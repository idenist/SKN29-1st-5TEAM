import streamlit as st
from streamlit_option_menu import option_menu

# ============================================
# 1. 사이드바 (Sidebar) 사용하기
# ============================================
# sidebar.py

def sidebar():
    st.sidebar.title("🚥 메뉴 이동")

    with st.sidebar:
        choice = option_menu(
            "Menu", 
            [
                "메인 홈", 
                "맞춤형 자동차 통계", 
                "연도별 등록 추이", 
                "휴게소 정보",       # 👈 데이터/리스트용
                "휴게소 위치 지도", # 👈 지도 시각화용
                "FAQ 게시판"
            ],
            # 아이콘도 각각 어울리는 걸로 배치했습니다.
            icons=['house', 'car-front', 'graph-up', 'info-circle', 'map', 'question'],
            menu_icon="app-indicator", default_index=0,
            styles={
                "container": {"padding": "4!important", "background-color": "#fafafa"},
                "icon": {"color": "black", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
                "nav-link-selected": {"background-color": "#08c7b4"},
            }
        )
    
    return choice