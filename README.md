# FinPin_LangchainTon
[아이펠 데이터사이언티스트 3기 랭체인톤] 금융핀_AI 기반 금융 뉴스 요약 솔루션

![gif-ezgif com-crop](https://github.com/user-attachments/assets/c8e4f75e-2721-4205-90a4-1527a1482b27)

<br>

## 팀원
<table>
  <tr>
    <td>
        <a href="https://github.com/Kyungdeok-Koo">
         <img src = "https://avatars.githubusercontent.com/u/184886763?v=4" width="100px" />  
        </a>
    </td>
    <td>
        <a href="https://github.com/hayannn">
         <img src = "https://avatars.githubusercontent.com/u/102213509?v=4" width="100px" />  
        </a>
    </td>
   <td>
        <a href="https://github.com/EstherJi07">
         <img src = "https://avatars.githubusercontent.com/u/180496208?v=4" width="100px" />  
        </a>
    </td>
  </tr>
  <tr>
    <td><b>👑구경덕</b></td>
    <td><b>이하얀</b></td>
    <td><b>지은현</b></td>
  </tr>
   <td><a href="https://github.com/Kyungdeok-Koo">Kyungdeok-Koo</a></td>
   <td><a href="https://github.com/hayannn">hayannn</td>
   <td><a href="https://github.com/EstherJi07">EstherJi07</td>
  </tr>
   <tr>
   <td> - </td>
    <td><a href="https://velog.io/@dlgkdis801"/>velog</td>
    <td> - </td>
    
  </tr>
</table>

<br>

## 개요
### 주제
- 금융 뉴스 요약 프로젝트
  - 여러 뉴스 사이트에서 제공하는 데이터셋(네이버, 구글 등)을 기반으로 금융 뉴스를 요약

### 문제
- 여러 사이트들을 보면서 자료를 수집하는 데에 시간적인 낭비가 심함
- ChatGPT의 요약 도움
  - 제대로 잘 요약되지 않는 부분이 많아 불편함을 자주 느낌
  - 출처 등이 명확하지 않아 다소 신뢰도가 떨어짐
 
### 목표
- MVP 모델 제작
  - Naver Search API를 이용하여 데이터 로드 및 검색
  - OpenAI 임베딩 및 LLM을 통한 데이터 분할 및 임베딩, 검색 과정을 거쳐 답변을 생성
  - 사용자가 더욱 쉽게 경제 뉴스를 접할 수 있고, 빠르게 신뢰성 있는 정보를 파악할 수 있도록 함

<br>

## 데이터 & 기술스택
- Python
- Naver Search API
- OpenAI API
- spaCy(ko_core_news_sm)
- LangChain
    - ChatOpenAI
    - OpenAIEmbeddings
    - RetrievalQA
    - Chroma
- Streamlit
<br>

## 디렉터리 구조
```
├── 📑 README.md
├── 📑 .gitignore         # gitHub 저장소에 올라가지 않아야 하는 파일 설정
├── 📑 requirement.txt    # 설치 파일 목록
├── 🗂️ docs               # Notion 자료, BackLog, Appendix 내용 업로드
|   └── ...
|
├── 📑 fetch_news.py      # Naver Search APi 사용 스크립트
└── 📍 finpin.py          # 메인 앱 파일
```
<br>
<br>

## 서비스 아키텍쳐
이미지 첨부 예정

<br>
<br>

## 주요 기능
### 날짜와 키워드를 기반으로 한 금융 뉴스 검색 기능 ➡️ 날짜를 다양하게 입력해도 일관되게 인식!
- 💬 2025년 1월 15일의 금융 뉴스를 알려줄래?
- 💬 25년 1월 15일 금융 관련 뉴스를 알려줘.
- 💬 1월 15일 금융 뉴스
- 💬 15일 금융 뉴스는?

### 키워드 입력을 통해 최근 뉴스를 모아볼 수 있는 기능
- 💬 최신 금융 동향은?
- 💬 최근 비트코인 관련 동향?
- 💬 최근 금융 시장에 대한 주요 업데이트를 알려줘.

### 과거 날짜의 기사 확인 기능
- 💬 1월 2일 금융 뉴스는?
- 💬 1월 2일 ETF 뉴스는?

### 입력을 자유롭게 하더라도, 키워드를 감지하는 기능
- 💬 2025년 1월 15일의 ETF 뉴스를 알려줄래?
- 💬 1월 15일 코스피 뉴스
- 💬 2일 증시 뉴스는?
- 💬 2025년 1월 6일 해외주식 관련 뉴스는?
- 💬 최근 소비자물가 동향을 알려줘.

<br>
<br>

## 특징
### 1. 기존 ChatGPT의 할루시네이션 현상 방지
정확한 출처의 기사만을 인용하여 거짓된 자료 및 요약 생성을 하지 않음

<br>

### 2. 전체 요약 출력 및 기사 1개당 1개의 카드로 "제목, 날짜, 요약, 원문보기" 구성
기사들을 분석해 나온 전체 요약을 우선 출력
<br>
그 후, 기사 1개당 1개의 카드로 볼 수 있도록 하여 각 제목과 날짜, 요약, 원문보기를 이용한 기사 링크 접속 가능 

<br>
<br>

## 실행 방법
### 0. 사전 준비
OpenAI API Key와 Naver Open API ID, Secret Key 필요
- 🔗 [OpenAI API Key 발급 사이트](https://platform.openai.com/api-keys)
- 🔗 [Naver Open API Key 발급 사이트](https://developers.naver.com/main/)

Python 3.11.2 버전 설치 필요
- 🔗 [Python Install 사이트](https://www.python.org/downloads/release/python-3112/)

<br>

### 1. 저장소 클론
해당 저장소를 로컬 PC에 클론하여 저장
```
git clone https://github.com/hayannn/FinPin_LangchainTon.git
```

### 2. .env 파일 추가
OpenAI API Key와 Naver Search API CLIENT ID, SECRET Key 입력
```
OPENAI_API_KEY={실제키입력}
NAVER_CLIENT_ID={네이버 애플리케이션을 통해 발급받은 ID}
NAVER_CLIENT_SECRET={네이버 애플리케이션을 통해 발급받은 secret key}
```

### 3. 패키지 설치
해당 프로젝트에 필요한 패키지 목록을 이용해 설치
```
pip install -r requirements.txt
```

### 4. 앱 실행
금융 뉴스 요약 챗봇을 실행
```
streamlit run finpin.py
```

<br>
<br>

## 챗봇 검증 방법
### 동일한 질문을 기반으로 기본 ChatGPT 모델 요약 답변과 프로젝트 모델 요약 답변을 비교하는 방식으로 검증
- 유사한 질문을 계속해서 던질 경우, 동일한 답변을 내는지 여부
  - 사용자가 입력하는 날짜 형식이 다를 수 있어, 유연하게 대응이 되는지 확인
- 키워드를 잘 감지하고, 비슷한 질문에 일관된 답변을 가져오는지 확인
- 당일이 아닌 다른 날짜의 자료도 잘 가져오는지 확인
- 키워드를 다양하게 적용했을 경우의 결과 확인
- 답변 결과의 가시성 비교
- 레퍼런스 연결 신뢰도 비교

<br>
<br>

## 시연 영상
추후 업로드

<br>
<br>

## 향후 발전 방향
### 1. API 종류 확장
네이버 검색 API뿐만 아니라, 다른 플랫폼에서 제공하는 API 또는 자료 적용을 통해 더 다양한 정보 제공

<br>

### 2. 요약 내용에 기초 금융 용어에 대한 설명을 추가해주는 것
단순 웹 검색이 아닌 신뢰성 있는 정보에서 추출해주는 방식

<br>

### 3. 금융뿐만 아니라 다른 분야에 특화된 모델로도 발전 가능

<br>

### 4. 요약 내용 개선 및 오타에 대한 유연성
첨부한 기사들을 기반으로 더 잘 요약된 "전체 요약"내용의 개선이 필요<br>
사용자 입력에 있어 기본적인 오타 또는 비정형 입력 등에 대한 처리가 있어야 할 것으로 보임
