# 데이터 기반 중고차 구매 의사결정 지원 서비스

---

## 팀 구성

<table align="center">
  <tr>
    <td align="center" width="190px"><img src="./picture/2h8XxT6hr24MKZFGBo2UW3ho7PZxHmedkIpORL9nEpu-aCK9SG6Q5Zb-PveW7qUMkXxdm9hi0Wb5aCxiOQCMAg (1).png" width="100" style="object-fit: contain; aspect-ratio: 1/1;"></td>
    <td align="center" width="190px"><img src="./picture/HBEyYPBCLGqnOQ7P-ElavftUeK1Orf3QENCcXk-5m6QIx2qqjSIpdB6XsdaKTdvE2nR2ngCNq5hiBKC_GhmNkg.png" width="100" style="object-fit: contain; aspect-ratio: 1/1;"></td>
    <td align="center" width="190px"><img src="./picture/fjG_du5l4xE1o_v_AmZWztwKi6XNGT_W0AdTmjV17wQV1j7PHK4bdMe1nJ2E47i7sPuXJp1Pmod-Di4Gq7q_Kw.png" width="100" style="object-fit: contain; aspect-ratio: 1/1;"></td>
    <td align="center" width="190px"><img src="./picture/EVQ1qeevGhLxkMJjLFrD_xf_pfwSCUN-NftYAvC9QdtHMWr2Z9FhWzTPxKLJUjNHd2qnBWo5PKr0FhwzYHL9RQ.png" width="100" style="object-fit: contain; aspect-ratio: 1/1;"></td>
  </tr>
  <tr>
    <td align="center"><b>윤대성</b></td>
    <td align="center"><b>윤승혁</b></td>
    <td align="center"><b>최지용</b></td>
    <td align="center"><b>한예나</b></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/YoonDaesung-01"><img src="https://img.shields.io/badge/YoonDaesung--01-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
    <td align="center"><a href="https://github.com/idenist"><img src="https://img.shields.io/badge/idenist-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
    <td align="center"><a href="https://github.com/antisdream"><img src="https://img.shields.io/badge/antisdream-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
    <td align="center"><a href="https://github.com/hanyena0830"><img src="https://img.shields.io/badge/hanyena0830-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
  </tr>
</table>
                                

---
## 실행 환경 (Environment)
> [requirements.txt](path/requirements.txt)를 참조
---
## 실행 방법 (How to Run)

### 1) 환경변수 설정

- `.env'에 ""안에는 호스트로부터 제공받은 값을 입력합니다.
- 필요 변수: DB_HOST="", DB_PORT="", DB_USER="", DB_PASSWORD="", DB_NAME_CARMASTER=""
DB_NAME_VEHICLE_YEAR="", DB_NAME_FAQ="", DB_NAME_TRAFFIC=", ITS_API_KEY=""
---
### 2) streamlit 실행
  프로젝트 폴더의 최상단 위치에서 다음 명령어를 실행한다.
```
<bash>
streamlit run app.py
```
---
## ERD
<img alt="image" src="./picture/ERD.png">
---

## 구현 화면 (Demo)
### 1) 메인 홈

<img width="1478" height="471" alt="image" src="./picture/readme main background.png" />

txt : 부트캠프 기수, 조 이름, 슬로건, Web 안내사항
btn : sidebar menu(메인 홈, 등록된 자동차 통계, 연도별 등록 추이, 연도별 고속도로 통행량, 주요 지역 소요 시간, 휴게소 위치 지도, FAQ 게시판)

---

### 2) 등록된 자동차 통계
       (최근 5개월 자동차 신규 등록 통계)

<img alt="image" src="" />

> 1. 항목 분석
  연료별, 차종별, 성별, 연령대별, 국산/외산 비중을 확인 가능 

> 2. 각 항목 월별 분석
  최근 5개월 자동차 신규 등록 통계를 나타내고 있으며,
  연료별, 차종별, 성별, 연령대별, 국산/외산 비중을 확인 가능 

---

### 3) 연도별 등록 추이
       (연도별 자동차 등록 현황 (2017~2025))

<img width="1911" height="836" alt="image" src="" />


> 1. 연도별 자동차 등록
  연도별 전체 합계 꺾은선 그래프와 연도별 차종 누적 등록 대수의 막대형 그래프를 확인 가능

> 2. 연도별 상세 분석
  원하는 연도를 선택하여 파이그래프 형식으로 차종별 비중과 용도별 비중을 확인 가능

---

### 4) 연도별 고속도로 통행량
       (연도별 고속도로 통행량 변화)

<img width="1911" height="836" alt="image" src="" />

> 2017년 ~ 2025년 교통량 변화에 관한 꺾은선 그래프

---

### 5) 주요 지역 소요시간
       (주요 도시 소요시간)

<img width="1911" height="836" alt="image" src="" />


> 서울에서 출발하는 주요 대표 노선, 서울로 도착하는 주요 대표 노선, 기타 노선에 관한 소요시간과 실시간 CCTV 정보

---

### 6) 휴게소 위치 지도
       (노선별 휴게소 정보)

<img width="1911" height="836" alt="image" src="" />


> 각 노선별 항목을 클릭하면 휴게소 명단이 출력되며,
  명단에서 원하는 휴게소 또는 지도에서 원하는 휴게소를 선택하면 그 휴게소에 대한 정보 출력

---

### 7) FAQ 게시판
       (통합 FAQ 게시판)

<img width="1911" height="836" alt="image" src="" />


> 1. 현대자동차
  모젠 서비스, 블루링크, 정비예약, 차량구매, 차량정비, 특허관련, 현대 디지털 키, 홈페이지 FAQ

> 2. 기아자동차
  PBV, 기아멤버스, 기타, 차량 구매, 차량 정비, 홈페이지 FAQ

> 3. 하이패스
  EX모바일충전카드, EX선불카드, 단물기등록, 하이패스서비스

---

## 1. 프로젝트 개요

### 1.1 프로젝트 요약

기 : 해마다 꾸준히 증가하는 자동차 등록대수로 인한 고속도로 통행량 증가 발생
승 : 고속도로를 이용하는 운전자들의 단순 길 안내를 넘어 고속도로 이용 중 편리한 정보의 제공이 필요
전 : 그 중 휴게소는 단순 휴식공간이 아닌 운전자들에게 다양한 정보 및 콘텐츠를 제공함
결 : 자동차 등록대수 증가로 인한 운저자들의 고속도로 정보가 필요하기 때문에 휴게소 및 고속도로 내의 정보 제공이 필요하다는 타당성

---

### 1.2 문제 정의

요즘에는 고속도로 내에 위치한 휴게소를 목적지에 가기위해 거쳐가는 곳으로만 이용하지 않고, 다양한 컨텐츠를 즐기러 가기위한 사람들이 증가되고 있음에도 불구하고 정보를 알 수 있는 방법이 한정적이거나 복잡함

---

### 1.3 프로젝트 실행
#### 1.3.1 환경설정 파일 생성 및 확인
`git local`폴더 안에 `.env`파일을 생성한 후에 아래의 예시대로 작성해야 한다.
```.env
DB_HOST="", DB_PORT="", DB_USER="", DB_PASSWORD="", DB_NAME_CARMASTER=""
DB_NAME_VEHICLE_YEAR="", DB_NAME_FAQ="", DB_NAME_TRAFFIC=", ITS_API_KEY=""
```

#### 1.3.2 docker-compose 실행
프로젝트 폴더의 최상단 위치에서 아래의 명령어를 실행한다.
```bash
docker-compose -p skn29_1st_5team up 
```
- `-p SKN29-1ST-TEAM`: Docker Compose의 프로젝트 이름 지정
- 컨테이너, 네트워크, 저장소 이름이 SKN29-1ST-5TEAM_* 형태로 생성됨

---

## 2. 서비스 설계 철학

핵심 설계 원칙은 다음과 같다.

1. **공공데이터를 사용하여 정보의 정확성을 전달한다.**
    - 대략적으로 예측한 정보가 아닌 정확하게 통계를 낸 정보를 반영한다.
2. **설명 가능한 모델만 사용한다.**
    - 복잡한 모델보다 해석 가능한 거리 함수, 회귀, 분위수 기반 판정을 채택한다.
3. **정보는 직관적으로 제시할 수 있어야 한다.**
    - 사용자가 원하는 정보를 손쉽게 얻을 수 있도록 시각화를 설계한다.

---

## 3. 핵심 기능

| 구분         | 기능                       | 설명                                          |
|-------------|---------------------------|-----------------------------------------------|
| 동적 크롤링   | CCTV 및 연료값 실시간 연동  | 1시간 내지 간격으로 실시간 정보 확인 가능           |
| 시각화       | map에 option추가          | 각 휴게소별 제공하는 컨텐츠 정보 확인 가능           |
| 시각화       | 연도별 차량 등록 대수 증가   | 연도별 차량 등록 대수 증가를 항복멸 확인 가능        |

---

## 4. 시스템 아키텍처

```
공공데이터 크롤링 → MySQL → Python 분석 → Streamlit 서비스
한국도로공사 크롤링 → MySQL → Python 분석 → Streamlit 서비스
국가데이터처 크롤링 → MySQL → Python 분석 → Streamlit 서비스
```

데이터 수집, 저장, 분석, 시각화 단계를 분리하여 확장성과 유지보수성을 확보함.

---

## 5. 데이터 수집 및 정제

### 5.1 데이터 출처

- 공공데이터 포털, 한국도로공사, 국가데이터처 각 사이트별 Open API에서 크롤링

### 5.2 수집 항목

- **자동차 등록 대수**
    - 연도별 등록 대수
    - 월별 등록 대수
    - 연료별
    - 차종별
    - 성별
    - 연령대별
    - 국산/외산
- **고속도로 정보 관련**
    - 연도별 고속도로 통행량
    - 고속도로 실시간 CCTV
    - 실시간 주요 도시 통행 소요시간
- **휴게소 정보 관련**
    - 휴게소 위치 좌표
    - 휴개소 내 주유소의 실시간 연료값
    - 휴게소 내 컨텐츠 정보
    - 휴게소 내 행사 정보

### 5.3 전처리

- **수치 정규화**
    - 주유값 정수 변환

- **도메인 전처리**
    - 컬럼명을 영어에서 한글로 변환

---

## 6. 데이터베이스 설계
### 6.1 개념 모델 설계
#### 요구 정의서
  - 목적: 고속도로 휴게소 정보, 차량 통계, 연도별 통행량, 구간별 소요시간, FAQ를 통합 제공
  - 주요 기능: 휴게소 위치 조회 및 지도 표시, 연도별/구간별 통계 시각화, 통행량 분석, 소요시간 분석, FAQ.
  - 데이터 출처: 교통 센서/도로공사 API, 공공데이터(통행량·휴게소 목록), 내부 수집(사용자 업로드 CSV), 스케줄링된 배치 수집.

#### 6.1.1 개념 엔티티 정의
  - RestArea: 휴게소(아이디, 이름, 위도, 경도, 도로명, 편의시설 목록, 운영시간)
  - TrafficCount: 통행량(아이디, 휴게소 또는 구간 참조, 측정일시, 차량수, 차종구분)
  - VehicleRegistration: 등록차량 통계(아이디, 연도, 지역, 등록대수, 차량종류)
  - TravelTime: 구간 소요시간(아이디, 구간ID, 측정일시, 평균소요시간, 표준편차)
  - FAQ: 기본적인 안내사항
  - Amenities: 휴게소 편의시설 표준화 테이블(편의시설ID, 이름, 카테고리)

#### 6.1.2 개념 관계
  - RestArea 1 : N TrafficCount (한 휴게소에 여러 통행량 기록)
  - RestArea 1 : N TravelTime (휴게소 인근 구간의 소요시간 기록)
  - Region 1 : N VehicleRegistration (지역별 연도별 등록 통계)

---

### 6.2 논리 모델 설계

```
핵심 테이블 스키마 예시 (논리 모델)
TABLE RestArea (
  rest_area_id SERIAL PRIMARY KEY,
  name VARCHAR(200),
  latitude DECIMAL(9,6),
  longitude DECIMAL(9,6),
  road_name VARCHAR(200),
  amenities JSONB,
  open_hours VARCHAR(100),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

TABLE TrafficCount (
  traffic_id SERIAL PRIMARY KEY,
  rest_area_id INT REFERENCES RestArea(rest_area_id),
  measured_at TIMESTAMP,
  vehicle_count INT,
  vehicle_type VARCHAR(50),
  source VARCHAR(100)
);

TABLE TravelTime (
  travel_time_id SERIAL PRIMARY KEY,
  segment_id VARCHAR(100),
  rest_area_id INT REFERENCES RestArea(rest_area_id),
  measured_at TIMESTAMP,
  avg_travel_time_sec INT,
  stddev_travel_time_sec INT
);

TABLE VehicleRegistration (
  reg_id SERIAL PRIMARY KEY,
  year INT,
  region VARCHAR(100),
  vehicle_type VARCHAR(50),
  registered_count INT
);

TABLE FAQ (
  faq_id SERIAL PRIMARY KEY,
  title VARCHAR(300),
  content TEXT,
  author VARCHAR(100),
  tags VARCHAR(200),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```
---

### 6.3 물리 모델 설계
#### 6.3.1 데이터 베이스
6.3.1 데이터 베이스
- 권장 DBMS: PostgreSQL (PostGIS 확장 사용 권장)
- 저장소 설계:
- 공간 데이터: 휴게소 위치는 geometry(Point)로 저장, 공간 인덱스(GIST) 생성.
- 시간 시계열: 통행량·소요시간은 파티셔닝(예: 연도별 또는 월별) 적용.
- JSONB: 편의시설 등 가변 속성은 JSONB로 저장하여 유연성 확보.
- 인덱스: rest_area_id, measured_at, 공간 인덱스, 자주 조회되는 조합 컬럼 복합 인덱스 생성.
- 백업/복구: 정기 스냅샷 및 WAL 아카이빙.
- 접근 제어: 최소 권한 원칙, DB 사용자별 권한 분리.

---

## 7. 데이터 파이프라인
  1. 수집 (Ingest)
    - 실시간/주기적 API 호출: 도로공사/공공데이터 API
    - 센서/로그 수집: 교통 센서 스트림(옵션)
    - 배치 업로드: CSV/엑셀 파일 업로드 기능

  2. 수집 후 처리 (Preprocessing)
    - 스키마 정규화, 결측치 처리, 타임존 정리
    - 좌표계 통일(WGS84), 위경도 유효성 검사
    - 이상치 탐지(예: 차량수 급증) 및 플래그 처리

  3. 저장 (Storage)
    - 원시 데이터: 데이터 레이크 또는 별도 원본 테이블 보관
    - 정제 데이터: 분석용 테이블로 적재 (PostgreSQL/PostGIS)

  4. 변환 및 집계 (Transform)
    - 일/주/월 단위 집계 작업 (Airflow/Cron)
    - 이동 평균, 표준편차, 피크 시간대 계산

  5. 모델/분석 (Modeling)
    - 군집화, 유사도 계산, 예측 모델(선택)

  6. 제공 (Serve)
    - Streamlit 앱에서 쿼리 및 시각화
    - API 엔드포인트(선택)로 외부 제공

  7. 모니터링
    - 파이프라인 실패 알림, 데이터 품질 대시보드
---

## 8. 유사도 기반 군집화 모델 설계

### 8.1 군집(비교군) 구성 원칙
  - 목표: 휴게소 또는 구간을 트래픽 패턴·편의시설·위치 특성에 따라 그룹화하여 비교군(benchmark) 제공.
  - 특성(피처):
  - 시간대별 평균 통행량(피크/비피크), 요일 패턴
  - 편의시설 수치화(주유소, 음식점, 화장실 등)
  - 위치 특성(고속도로 종류, 인접 도시 인구)
  - 소요시간 통계(평균, 분산)
  - 스케일링: 각 피처는 표준화 또는 정규화 적용.
  - 알고리즘: K-Means, DBSCAN(밀도 기반), 계층적 군집화 중 목적에 맞게 선택.
  - 평가 지표: 실루엣 점수, 군집 내 분산, 도메인 전문가 검토.

### 8.2 군집화를 ‘설명 가능한 방식’으로 설계한 이유
  - 해석성: 운영자와 의사결정자가 군집 기준(예: 트래픽 패턴, 편의시설)으로 이해하고 활용할 수 있어야 함.
  - 투명성: 피처 가중치와 거리 함수를 명시하여 결과를 재현 가능하게 함.
  - 운영 적용성: 군집 결과를 휴게소 추천, 인프라 투자 우선순위 결정에 직접 연결하기 위함.


---

## 9. 관련 선행 연구 요약

  - 교통 패턴 분석: 시간대·요일별 통행량 패턴을 이용한 군집화 연구가 다수 존재하며, 피크 시간대 모델링이 핵심.
  - 휴게소 서비스 최적화: 편의시설과 트래픽을 결합한 서비스 배치 연구는 휴게소 만족도 향상에 기여.
  - 설명 가능한 ML: SHAP, LIME 등을 통해 피처 기여도를 제시하면 운영 의사결정에 신뢰성 제공.

---
## 10. 가격 점수(Price Score) 
  - 목적: 휴게소 내 유료 서비스(주유, 음식, 주차 등)의 상대적 가치를 수치화하여 사용자에게 추천 우선순위를 제공.
  - 제안식(예시):
  \mathrm{PriceScore}=w_1\cdot \frac{\mathrm{서비스가격}}{\mathrm{지역평균가격}}+w_2\cdot (1-\frac{\mathrm{대기시간}}{\mathrm{최대대기시간}})+w_3\cdot \mathrm{편의성점수}
  - 구성요소:
  - 서비스가격 대비 지역 평균: 가격 경쟁력 반영
  - 대기시간: 짧을수록 점수 상승
  - 편의성점수: 편의시설 수, 청결도, 접근성 등 정성적 지표를 정량화
  - 가중치: w_1,w_2,w_3는 도메인 요구에 따라 조정.

---

## 11. 서비스 UI 흐름
- 사이드바 메뉴 구조 (app.py 기준)
- 메인 홈 (Hero 이미지)
- 등록된 자동차 통계 (show_stats)
- 연도별 등록 추이 (show_yearly_stats)
- 연도별 고속도로 통행량 (page_traffic.show_page)
- 주요 지역 소요 시간 (page_traffic_time.show_page)
- 휴게소 정보 (휴게소 상세 페이지; 현재 미구현)
- FAQ 게시판 (show_faq)
- 휴게소 위치 지도 (page_map.show_rest_area_map)
- 페이지별 핵심 UI 요소
- 메인 홈: 대형 히어로 배너, 주요 KPI 카드(총 휴게소 수, 최근 피크 시간 등)
- 통계 페이지: 필터(연도, 지역), 시계열 차트, 표 다운로드 버튼
- 통행량 페이지: 구간 선택, 히트맵/라인차트
- 소요시간 페이지: 구간별 평균·분산, 지도 오버레이
- 휴게소 지도: 클러스터 마커, 팝업에 편의시설·평점 표시
- FAQ: 질문 검색, 카테고리 필터, 관리자 답변 기능

---

## 12. GitHub 폴더 구조
```
PROJECT_1/

├── Crawling/                  # 크롤링 및 데이터 수집 관련 폴더

│   ├── dynamic_crw.ipynb      # FAQ 데이터 크롤링 

│   ├── rest_area2.ipynb       # 휴게소 데이터 정보 수집

│   ├── rest_event.ipynb       # 휴게소 이벤트 데이터 수집

│   ├── rest_gas.ipynb         # 휴게소 주유소 데이터 수집

│   ├── traffic_forecast.ipynb # 교통 예상 시간 데이터 수집

│   └── traffic_upload.py      # 교통 데이터 업로드 스크립트

├── page/                      # Streamlit 각 페이지 모듈 폴더

│   ├── page_faq.py            # FAQ 페이지

│   ├── page_map.py            # 휴게소 위치 지도 페이지

│   ├── page_stats.py          # 자동차 및 통계 페이지

│   ├── page_traffic_time.py   # 주요 지역 소요 시간 페이지

│   └── page_traffic.py        # 고속도로 통행량 페이지

├── picture/                   # 이미지 리소스 폴더

│   ├── ERD.png                # 데이터베이스 설계도

│   ├── highway.png            # 고속도로 배경 이미지

│   ├── readme main background.png # README용 배경 이미지

│   └── (기타 이미지 파일들...)

├── .env                       # 환경 변수 설정 파일 (API 키 등)

├── .gitignore                 # Git 제외 대상 설정 파일

├── app.py                     # Streamlit 메인 실행 파일

├── requirements.txt           # 설치 필요한 라이브러리 목록

├── sidebar.py                 # 사이드바 메뉴 구성 모듈

└── utils.py                   # 공통 유틸리티 함수 모듈

---
```
## 13. 프로젝트 차별성

  - 통합 뷰: 휴게소 위치·편의시설·실시간 통행량·소요시간을 한 화면에서 결합 제공.
  - 설명 가능한 군집화: 단순 블랙박스가 아닌 피처 기반 설명을 제공하여 운영 의사결정에 활용 가능.
  - 경량 배포: Streamlit 기반으로 빠른 프로토타이핑 및 데모 배포 가능.
  - 공간 분석 지원: PostGIS 연동을 통한 공간 쿼리 및 지도 시각화 최적화.

---

## 14. 한계점

  - 데이터 가용성 의존: 공공 API 또는 센서 데이터 품질에 따라 분석 정확도가 달라짐.
  - 실시간성 제약: 현재 구조는 주기적 배치에 최적화되어 있어 초저지연 실시간 분석에는 추가 설계 필요.
  - 스케일링: 대량의 시계열 데이터(수천·수만 센서) 처리 시 DB 파티셔닝·아카이빙 전략 필요.
  - 편의시설 정성평가 한계: 편의성 점수는 주관적 요소가 포함될 수 있어 표준화 필요.

---

## 15. 확장 방향

  - 실시간 스트리밍 파이프라인: Kafka/Fluentd + 스트림 처리(예: Spark Streaming)로 실시간 대시보드 구현.
  - 예측 모델: 통행량·소요시간 예측(시계열 모델, LSTM/Prophet)으로 사전 알림 제공.
  - 사용자 피드백 루프: 앱 내 평점·리뷰 수집으로 편의시설 점수 보정.
  - 모바일 최적화: 반응형 UI 또는 PWA로 모바일 접근성 강화.
  - API 서비스화: 외부 앱/서비스가 활용할 수 있도록 REST/GraphQL API 제공.
  - 권장 기능: 휴게소 혼잡 예측, 최적 휴게소 추천(경로·시간 기반).

---
