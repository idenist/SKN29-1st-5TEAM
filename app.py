import streamlit as st

# 🌟 분리해 둔 화면 함수들을 불러옵니다!
from page_faq import show_faq
from page_stats import show_stats, show_yearly_stats  # 👈 show_yearly_stats 추가!
from page_traffic import show_page
import page_map  # 새로 만든 지도 페이지 모듈
from sidebar import sidebar
from PIL import Image 

# 페이지 기본 설정
st.set_page_config(page_title="통합 플랫폼 대시보드", page_icon="🚥", layout="wide")

# 👈 메뉴에 '연도별 등록 추이'를 추가했습니다.
menu = sidebar()

st.markdown("""
<style>
.toc-btn,
.toc-btn:link,
.toc-btn:visited,
.toc-btn:hover,
.toc-btn:active {
    display: block;
    width: 100%;
    padding: 0.75rem 1rem;
    margin: 0.4rem 0;
    border-radius: 0.7rem;
    border: 1px solid rgba(49, 51, 63, 0.2);
    background: white;
    color: rgb(49, 51, 63);
    text-decoration: none !important;
    font-weight: 600;
    font-size: 1.05rem;
    box-sizing: border-box;
}

.toc-btn:hover {
    border-color: rgb(255, 75, 75);
    color: rgb(255, 75, 75);
    text-decoration: none !important;
}
</style>
""", unsafe_allow_html=True)
    
# 메인 화면 로직 분기
if menu == "메인 홈":
    st.header("👋 HI-REST에 오신 것을 환영합니다 😍")
    col1, col2 = st.columns(2)

    # 2. 첫 번째 컬럼에 내용 추가
    with col1:
        my_image = Image.open('./highway.avif')
        st.image(my_image)

    # 3. 두 번째 컬럼에 내용 추가
    with col2:
        # 목차
        st.markdown("""
        <a class="toc-btn" href="#car-status">자동차 등록 현황</a>
        <a class="toc-btn" href="#highway-status">고속도로 이용 현황</a>
        <a class="toc-btn" href="#rest-status">휴게소 현황</a>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.subheader("📍 HI-REST란?")
    st.markdown("""
        국가데이터처에서 제공하는 데이터에 따르면 누적 자동차등록대수는 근 10년간 꾸준히 증가해왔습니다.  
        이는 자동차를 이용한 이동 수요가 점차 증가하고 있다는 점을 의미하고,  
        자동차를 통한 이동 수요가 많아진다는 것은 고속도로의 이용량이 점차 늘어난다는 의미도 됩니다.  
        
        """)

elif menu == "등록된 자동차 통계":
    show_stats() # 기존 carmaster_db 데이터 화면

elif menu == "연도별 등록 추이":
    show_yearly_stats() # 👈 신규 vehicle_db_year 데이터 화면

elif menu == "연도별 고속도로 통행량":  # 👈 사용자가 이 메뉴를 클릭하면
    show_page()
    
elif menu == "휴게소 정보":
    pass
    
elif menu == "FAQ 게시판":
    show_faq() 

elif menu == "휴게소 위치 지도":
    # 새로 만든 page_map.py 안의 함수를 호출!
    page_map.show_rest_area_map()