import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# DB 접속 정보만 .env에서 가져옵니다.
load_dotenv()

def upload_traffic_data():
    # --- 경로 지정 ---
    # 현재 파이썬 파일이 있는 위치의 'highway_traffic.csv'를 찾습니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_dir, 'highway_traffic.csv')

    # 1. CSV 데이터 존재 확인 및 로드
    if not os.path.exists(csv_file_path):
        print(f"❌ 오류: '{csv_file_path}' 파일을 찾을 수 없습니다.")
        print("CSV 파일과 파이썬 파일을 같은 폴더에 넣어주세요!")
        return

    try:
        df = pd.read_csv(csv_file_path)
        print(f"✅ CSV 데이터 로드 완료 ({len(df)}개 행)")

        # 2. DB 접속
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME_TRAFFIC"),
            port=int(os.getenv("DB_PORT", 3306)),
            charset="utf8mb4"
        )
        cursor = conn.cursor()

        # 3. 데이터 삽입 쿼리 (이미 있으면 통행량만 최신으로 업데이트)
        insert_sql = """
        INSERT INTO highway_traffic (traffic_year, vehicle_class, traffic_volume)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE traffic_volume = VALUES(traffic_volume);
        """

        # 데이터프레임의 행들을 튜플 리스트로 변환
        data_rows = [tuple(x) for x in df.values]

        # 일괄 삽입
        cursor.executemany(insert_sql, data_rows)
        conn.commit()
        
        print(f"🚀 성공: {cursor.rowcount}개의 데이터가 DB에 저장/업데이트되었습니다.")

    except Error as e:
        print(f"❌ DB 작업 중 오류 발생: {e}")
        if 'conn' in locals() and conn.is_connected():
            conn.rollback()
    except Exception as e:
        print(f"❌ 기타 오류 발생: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 DB 연결 종료")

if __name__ == "__main__":
    upload_traffic_data()