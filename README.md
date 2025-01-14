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
|
├── 📑 fetch_news.py      # Naver Search APi 사용 스크립트
└── 📍 finpin.py          # 메인 앱 파일
```
<br>

## 서비스 아키텍쳐

<br>

## 주요 기능


<br>

## 실행 방법


<br>

## 향후 발전 방향





