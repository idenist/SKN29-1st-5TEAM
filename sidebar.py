import streamlit as st
from streamlit_option_menu import option_menu

# ============================================
# 1. 사이드바 (Sidebar) 사용하기
# ============================================
def sidebar():
    st.sidebar.title("🚥 메뉴 이동")

    with st.sidebar:
        choice = option_menu(
            "Menu", ["메인 홈", "맞춤형 자동차 통계", "연도별 등록 추이", "휴게소 정보", "FAQ 게시판"],
            icons=['house', 'car-front', 'graph-up', 'p-circle', 'question'],
            menu_icon="app-indicator", default_index=0,
            styles={
                "container": {"padding": "4!important", "background-color": "#fafafa"},
                "icon": {"color": "black", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
                "nav-link-selected": {"background-color": "#08c7b4"},
            }
        )
    
    return choice