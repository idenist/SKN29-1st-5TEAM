import streamlit as st 

def main():
    tab1, tab2 = st.tabs(["자동차 등록 현황", "고속도로 이용 현황"])
    
    with tab1:
        st.header("🚘 연간 자동차 등록 현황")
        st.divider()
        
    with tab2:
        st.header("🛣️ 연간 고속도로 이용 현황")