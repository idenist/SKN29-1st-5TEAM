import streamlit as st
from streamlit_option_menu import option_menu

# ============================================
# 1. 사이드바 (Sidebar) 사용하기
# ============================================
def sidebar():
    st.sidebar.title("안녕하세요~")
    st.sidebar.write("5팀의 휴게소 프로젝트입니다")

    with st.sidebar:
        choice = option_menu(
            "Menu", ["메인 페이지", "연간 현황 정보", "휴게소 정보", "기업 FAQ"],
            icons=['house', 'car-front', 'p-circle', 'building'],
            menu_icon="app-indicator", default_index=0,
            styles={
                "container": {"padding": "4!important", "background-color": "#fafafa"},
                "icon": {"color": "black", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
                "nav-link-selected": {"background-color": "#08c7b4"},
            }
        )
    
    return choice