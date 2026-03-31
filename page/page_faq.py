import streamlit as st
from utils import load_data, render_pagination

def show_faq():
    st.title("❓ 통합 FAQ 게시판")
    st.write("궁금한 브랜드의 탭을 선택하고 카테고리 버튼을 클릭해 주세요.")
    
    tab_hyundai, tab_kia, tab_hipass = st.tabs(["🚙 현대자동차", "🚗 기아자동차", "💳 하이패스"])
    
    # [현대자동차 탭]
    with tab_hyundai:
        df_hyundai = load_data("hyundai_faq")
        if not df_hyundai.empty:
            st.markdown("### 🛠️ HYUNDAI FAQ")
            h_main_cats = sorted(df_hyundai['category_main'].unique())
            
            if 'h_selected_main' not in st.session_state:
                st.session_state.h_selected_main = h_main_cats[0] 

            cols = st.columns(6) 
            for i, cat in enumerate(h_main_cats):
                with cols[i % 6]:
                    btn_type = "primary" if cat == st.session_state.h_selected_main else "secondary"
                    if st.button(f"{cat}", key=f"h_main_{cat}", type=btn_type, use_container_width=True):
                        st.session_state.h_selected_main = cat
                        h_sub_cats_for_reset = sorted(df_hyundai[df_hyundai['category_main'] == cat]['category_sub'].unique())
                        st.session_state.h_selected_sub = h_sub_cats_for_reset[0]
                        st.session_state["hyundai_current_page"] = 1 
                        st.rerun() 

            st.markdown("---")
            h_sub_cats = sorted(df_hyundai[df_hyundai['category_main'] == st.session_state.h_selected_main]['category_sub'].unique())
            
            if 'h_selected_sub' not in st.session_state or st.session_state.h_selected_sub not in h_sub_cats:
                st.session_state.h_selected_sub = h_sub_cats[0]

            st.markdown("### 📌 소분류 선택")
            sub_cols = st.columns(6)
            for i, cat in enumerate(h_sub_cats):
                with sub_cols[i % 6]:
                    btn_type = "primary" if cat == st.session_state.h_selected_sub else "secondary"
                    if st.button(f"{cat}", key=f"h_sub_{cat}", type=btn_type, use_container_width=True):
                        st.session_state.h_selected_sub = cat
                        st.session_state["hyundai_current_page"] = 1
                        st.rerun()
            
            st.markdown("---")
            h_sel_main = st.session_state.h_selected_main
            h_sel_sub = st.session_state.h_selected_sub
            h_filtered = df_hyundai[(df_hyundai['category_main'] == h_sel_main) & (df_hyundai['category_sub'] == h_sel_sub)]
            
            h_search_kw = st.text_input("🔍 결과 내 검색 (질문/답변 포함)", key="h_search")
            if h_search_kw:
                h_filtered = h_filtered[
                    h_filtered['question'].str.contains(h_search_kw, case=False, na=False) |
                    h_filtered['answer'].str.contains(h_search_kw, case=False, na=False)
                ]

            st.caption(f"**{h_sel_main}** -> **{h_sel_sub}** 카테고리에서 **{len(h_filtered)}**개의 질문을 찾았습니다.")
            render_pagination(h_filtered, items_per_page=10, key_prefix="hyundai")
        else:
            st.info("데이터를 불러오는 중이거나 데이터가 없습니다.")

    # [기아자동차 탭]
    with tab_kia:
        df_kia = load_data("kia_faq")
        if not df_kia.empty:
            st.markdown("### 🛠️ KIA FAQ")
            k_cats = sorted(df_kia['category'].unique())
            
            if 'k_selected_cat' not in st.session_state:
                st.session_state.k_selected_cat = k_cats[0]

            cols = st.columns(6) 
            for i, cat in enumerate(k_cats):
                with cols[i % 6]:
                    btn_type = "primary" if cat == st.session_state.k_selected_cat else "secondary"
                    if st.button(f"{cat}", key=f"k_btn_{cat}", type=btn_type, use_container_width=True):
                        st.session_state.k_selected_cat = cat
                        st.session_state["kia_current_page"] = 1
                        st.rerun()
                    
            st.markdown("---")
            k_sel_cat = st.session_state.k_selected_cat
            k_filtered = df_kia[df_kia['category'] == k_sel_cat]
            
            k_search_kw = st.text_input("🔍 결과 내 검색 (질문/답변 포함)", key="k_search")
            if k_search_kw:
                k_filtered = k_filtered[
                    k_filtered['question'].str.contains(k_search_kw, case=False, na=False) |
                    k_filtered['answer'].str.contains(k_search_kw, case=False, na=False)
                ]

            st.caption(f"**{k_sel_cat}** 카테고리에서 **{len(k_filtered)}**개의 질문을 찾았습니다.")
            render_pagination(k_filtered, items_per_page=10, key_prefix="kia")
        else:
            st.info("데이터를 불러오는 중이거나 데이터가 없습니다.")

    # [하이패스 탭]
    with tab_hipass:
        df_hipass = load_data("hipass_faq") 
        if not df_hipass.empty:
            st.markdown("### 🛠️ HIPASS FAQ")
            hp_main_cats = sorted(df_hipass['category_main'].unique())
            
            if 'hp_selected_main' not in st.session_state:
                st.session_state.hp_selected_main = hp_main_cats[0]

            cols = st.columns(6) 
            for i, cat in enumerate(hp_main_cats):
                with cols[i % 6]:
                    btn_type = "primary" if cat == st.session_state.hp_selected_main else "secondary"
                    if st.button(f"{cat}", key=f"hp_main_{cat}", type=btn_type, use_container_width=True):
                        st.session_state.hp_selected_main = cat
                        hp_sub_cats_for_reset = sorted(df_hipass[df_hipass['category_main'] == cat]['category_sub'].unique())
                        st.session_state.hp_selected_sub = hp_sub_cats_for_reset[0]
                        st.session_state["hipass_current_page"] = 1
                        st.rerun()
            
            st.markdown("---")
            hp_sub_cats = sorted(df_hipass[df_hipass['category_main'] == st.session_state.hp_selected_main]['category_sub'].unique())
            
            if 'hp_selected_sub' not in st.session_state or st.session_state.hp_selected_sub not in hp_sub_cats:
                st.session_state.hp_selected_sub = hp_sub_cats[0]

            st.markdown("### 📌 FAQ 구분 선택")
            sub_cols = st.columns(6)
            for i, cat in enumerate(hp_sub_cats):
                with sub_cols[i % 6]:
                    btn_type = "primary" if cat == st.session_state.hp_selected_sub else "secondary"
                    if st.button(f"{cat}", key=f"hp_sub_{cat}", type=btn_type, use_container_width=True):
                        st.session_state.hp_selected_sub = cat
                        st.session_state["hipass_current_page"] = 1
                        st.rerun()
            
            st.markdown("---")
            hp_sel_main = st.session_state.hp_selected_main
            hp_sel_sub = st.session_state.hp_selected_sub
            hp_filtered = df_hipass[(df_hipass['category_main'] == hp_sel_main) & (df_hipass['category_sub'] == hp_sel_sub)]
            
            hp_search_kw = st.text_input("🔍 결과 내 검색 (질문/답변 포함)", key="hp_search")
            if hp_search_kw:
                hp_filtered = hp_filtered[
                    hp_filtered['question'].str.contains(hp_search_kw, case=False, na=False) |
                    hp_filtered['answer'].str.contains(hp_search_kw, case=False, na=False)
                ]

            st.caption(f"**{hp_sel_main}** -> **{hp_sel_sub}** 카테고리에서 **{len(hp_filtered)}**개의 질문을 찾았습니다.")
            render_pagination(hp_filtered, items_per_page=10, key_prefix="hipass")
        else:
            st.info("데이터를 불러오는 중이거나 데이터가 없습니다.")