import streamlit as st
from streamlit_option_menu import option_menu

def sidebar():
    st.sidebar.title("🚥 메뉴 이동")

    with st.sidebar:
        choice = option_menu(
            "Menu", 
            [
                "메인 홈", 
                "맞춤형 자동차 통계", 
                "연도별 등록 추이", 
                "연도별 고속도로 통행량",
                "주요 지역 소요 시간",
                "휴게소 위치 지도", 
                "FAQ 게시판"
            ],
            # 스톱워치(stopwatch) 아이콘을 추가로 배치했습니다.
            icons=['house', 'car-front', 'graph-up', 'bar-chart', 'stopwatch', 'map', 'question'],
            menu_icon="app-indicator", default_index=0,
            styles={
                "container": {"padding": "4!important", "background-color": "#fafafa"},
                "icon": {"color": "black", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
                "nav-link-selected": {"background-color": "#08c7b4"},
            }
        )
    
    return choice