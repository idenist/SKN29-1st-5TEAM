import streamlit as st
import mysql.connector
import os
import re
import pandas as pd
from dotenv import load_dotenv

# ==========================================
# 1. 기존 자동차 데이터 불러오기 (carmaster_db)
# ==========================================
@st.cache_data
def load_car_data():
    load_dotenv(override=True)
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'), 
            database=os.getenv('DB_NAME_CARMASTER') # .env에서 가져옴
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM car_registration_stats")
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return pd.DataFrame(data, columns=columns)
    except Exception as e:
        st.error(f"기존 자동차 DB 데이터 불러오기 실패: {e}")
        return pd.DataFrame()

# ==========================================
# 2. 🆕 신규 연도별 자동차 데이터 불러오기 (vehicle_db_year)
# ==========================================
@st.cache_data
def load_yearly_car_data():
    load_dotenv(override=True)
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'), 
            database=os.getenv('DB_NAME_VEHICLE_YEAR') # .env에서 가져옴
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicle_registrations")
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return pd.DataFrame(data, columns=columns)
    except Exception as e:
        st.error(f"연도별 자동차 DB 데이터 불러오기 실패: {e}")
        return pd.DataFrame()

# ==========================================
# 3. FAQ 데이터 불러오기 (faq_data)
# ==========================================
@st.cache_data
def load_data(table_name):
    load_dotenv(override=True)
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'), 
            database=os.getenv('DB_NAME_FAQ') # .env에서 가져옴
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return pd.DataFrame(data, columns=columns)
    except Exception as e:
        st.error(f"FAQ DB 데이터 불러오기 실패: {e}")
        return pd.DataFrame()

# ==========================================
# 4. 텍스트 정제 및 페이지네이션 (기존 코드 유지)
# ==========================================
def render_clean_answer(answer_text):
    if not answer_text:
        st.write("내용 없음")
        return

    clean_text = answer_text.replace('`', "'")
    clean_text = re.sub(r'\s*\n\s*([.,:;)])', r'\1', clean_text)
    clean_text = re.sub(r'([:,])\s*\n\s*', r'\1 ', clean_text)
    clean_text = re.sub(r'\s*\n\s*\(', ' (', clean_text)
    clean_text = re.sub(r'\(\s*\n\s*', '(', clean_text)
    clean_text = re.sub(r'\s*\n\s*/\s*\n\s*', ' / ', clean_text)
    clean_text = re.sub(r'\s*\n\s*/\s*', ' / ', clean_text)
    clean_text = re.sub(r'\s*/\s*\n\s*', ' / ', clean_text)
    clean_text = re.sub(r'(다\.|시오\.|요\.)\s*(?=[가-힣a-zA-Z①②③④⑤1-9])', r'\1\n\n', clean_text)
    clean_text = re.sub(r'\n\s*[-=]+\s*\n', '\n\n', clean_text)
    clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)
    
    parts = re.split(r'(\[이미지: .*?\])', clean_text)
    
    for part in parts:
        if part.startswith('[이미지:') and part.endswith(']'):
            img_url = part.replace('[이미지: ', '').replace(']', '').strip()
            try:
                st.image(img_url, use_container_width=True)
            except:
                pass
        else:
            if part.strip():
                part = re.sub(r'(?<!<)(https?://[a-zA-Z0-9./\-_?=&%]+)(?!>)', r'<\1>', part)
                safe_text = part.replace('\n#', '\n\#')
                formatted_text = safe_text.strip().replace('\n', '  \n')
                st.markdown(formatted_text)

def render_pagination(df, items_per_page=10, key_prefix=""):
    total_items = len(df)
    if total_items == 0:
        st.info("조건에 맞는 질문이 없습니다.")
        return

    total_pages = (total_items - 1) // items_per_page + 1
    page_key = f"{key_prefix}_current_page"
    
    if page_key not in st.session_state:
        st.session_state[page_key] = 1
    if st.session_state[page_key] > total_pages:
        st.session_state[page_key] = 1

    current_page = st.session_state[page_key]
    start_idx = (current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    paged_df = df.iloc[start_idx:end_idx]

    for _, row in paged_df.iterrows():
        question = row['question']
        if question.startswith("Q. "):
            question = question[3:]
        elif question.startswith("Q."):
            question = question[2:]
            
        with st.expander(question):
            render_clean_answer(row['answer'])

    if total_pages > 1:
        st.markdown("---")
        max_buttons = 5
        start_page = max(1, current_page - max_buttons // 2)
        end_page = min(total_pages, start_page + max_buttons - 1)
        
        if end_page - start_page + 1 < max_buttons:
            start_page = max(1, end_page - max_buttons + 1)
        
        num_buttons = end_page - start_page + 1
        cols = st.columns([1.5] + [0.5] + [0.5]*num_buttons + [0.5] + [1.5])
        
        with cols[1]:
            if st.button("◀", key=f"{key_prefix}_prev", disabled=(current_page == 1)):
                st.session_state[page_key] = current_page - 1
                st.rerun()
        
        for i, p in enumerate(range(start_page, end_page + 1)):
            with cols[2 + i]:
                btn_type = "primary" if p == current_page else "secondary"
                if st.button(str(p), key=f"{key_prefix}_btn_{p}", type=btn_type):
                    st.session_state[page_key] = p
                    st.rerun()

        with cols[2 + num_buttons]:
            if st.button("▶", key=f"{key_prefix}_next", disabled=(current_page == total_pages)):
                st.session_state[page_key] = current_page + 1
                st.rerun()