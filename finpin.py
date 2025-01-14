import streamlit as st
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai
from fetch_news import fetch_naver_news
import os
from dotenv import load_dotenv
from datetime import datetime
from bs4 import BeautifulSoup
import re
import spacy
from spacy.matcher import PhraseMatcher

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    print("API 키 로드 성공")
else:
    print("API 키 로드 실패")

embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

persist_directory = "./chroma_db"

# Streamlit
st.title("금융 뉴스 요약 챗봇 💬")
st.write("챗봇에 질문을 입력하면 최신 금융 뉴스를 요약하여 답변해드립니다!")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 최초 접속 시 인사말
if len(st.session_state.messages) == 0:
    st.session_state["messages"].append({"role": "assistant", "content": "안녕하세요! 질문을 입력해 주세요."})

# 이전 메시지 출력
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

# 사용자 입력
user_input = st.chat_input("질문을 입력해주세요🙂(ex.2025년 1월 13일의 금융 뉴스를 알려줄래?, 최신 금융 동향을 알려줘, ...)")

# spaCy 모델 로드 (한국어)
nlp = spacy.load("ko_core_news_sm")

# 특정 키워드 리스트
predefined_keywords = [
    'Tesla', 'Bitcoin', 'Stock', '경제', '금융', '주식', '테슬라', '비트코인', 
    '금리', '채권', '주식시장', '증권', '주식거래', 'ETF', '포트폴리오', '펀드', 
    '주식투자', '가상화폐', '크립토', '블록체인', '상장', '코스피', '코스닥', 
    '상장폐지', '상장주식', '배당', '주식배당', '시가총액', '이자율', '자산', 
    '자산운용', '리스크관리', '채권시장', '헤지펀드', '투자전략', '경제지표', 
    '물가', '소비자물가', '환율', '금융위기', '금융정책', '금융시스템', '국채', 
    '지수', '상승률', '하락률', '증시', '매수', '매도', '자산관리', '고배당주', 
    '금융상품', '부동산', '모기지', '대출', '채권금리', '금융기관', '거래소', 
    '리보금리', '금융규제', 'FOMC', 'IMF', 'OECD', 'GDP', '실업률', '인플레이션', 
    '유동성', '마진', '헤지', '옵션', '선물', '주식분석', '기업분석', '매출', '순이익', 
    '영업이익', '비즈니스모델', '가치투자', '성장투자', '워런버핏', '테크주', '그로쓰', 
    '인덱스펀드', '투자자', '주요지표', '저금리', '금융사기', '핀테크', '모바일뱅킹', 
    '디지털자산', '핀테크기업', '금융기술', '블록체인기술', '디지털화폐', '리브라', 
    '스테이블코인', '대체투자', '경기지표', '증권사', '금융컨설팅', '고정금리', 
    '변동금리', '국제금융', '금융분석', '경제위기', '경제성장', '고용지표', '상장기업', 
    '투자기회', '정책금리', '기준금리', '금융거래', '가치주', '성장주', '신용카드', 
    '해외주식', '자본시장', '중앙은행', '금융업계', '회계기준', '기업회계', '회계사'
]


# 사용자 입력에서 키워드를 추출하는 함수
def extract_keyword(text):
    """사용자 입력에서 키워드를 추출합니다."""
    doc = nlp(text)
    
    # PhraseMatcher를 사용하여 미리 정의된 키워드를 문장에서 찾기
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp.make_doc(keyword) for keyword in predefined_keywords]
    matcher.add("PredefinedKeywords", patterns)

    matches = matcher(doc)
    matched_keywords = [doc[start:end].text for _, start, end in matches]

    # 키워드가 있으면 추출하고, 없으면 None 반환
    if matched_keywords:
        return matched_keywords[0]  # 첫번째 키워드만 반환
    else:
        return None


# 날짜 추출 함수
def extract_date(text):
    """
    입력된 텍스트에서 날짜를 추출합니다.
    - "YYYY년 MM월 DD일", "MM월 DD일", "DD일" 등의 다양한 형식 지원
    - 형식이 없으면 None 반환
    """
    today = datetime.today()
    
    # 정규 표현식 패턴
    patterns = [
        (r"(\d{4})년 (\d{1,2})월 (\d{1,2})일", "%Y년 %m월 %d일"),  # YYYY년 MM월 DD일
        (r"(\d{1,2})월 (\d{1,2})일", "%m월 %d일"),                # MM월 DD일
        (r"(\d{1,2})일", "%d일")                                  # DD일
    ]
    
    for pattern, date_format in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                if date_format == "%d일":  # 날짜만 주어진 경우
                    day = int(match.group(1))
                    return today.replace(day=day)  # 이번 달의 해당 날짜 반환
                elif date_format == "%m월 %d일":  # 월과 날짜만 주어진 경우
                    month, day = map(int, match.groups())
                    return today.replace(month=month, day=day)
                else:  # YYYY년 MM월 DD일 형식
                    return datetime.strptime(match.group(), date_format)
            except ValueError:
                # 유효하지 않은 날짜일 경우 무시
                continue
    
    return None


# HTML 태그를 제거하는 함수
def clean_html(text):
    """HTML 태그를 제거합니다."""
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


# 기사 내용을 청크로 나누는 함수
def chunk_text(text, chunk_size=1000):
    """기사 내용을 1000자 이하로 청크로 나눕니다."""
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks


if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 날짜와 키워드 추출
    date = extract_date(user_input)
    keyword = extract_keyword(user_input)

    # 기본 쿼리
    query = user_input if not keyword else keyword

    # 날짜가 있으면 쿼리에 포함
    if date:
        query = f"{query} {date.strftime('%Y-%m-%d')}" # 날짜를 쿼리에 포함

    with st.spinner("네이버에서 뉴스 가져오는 중..."):
        try:
            # 뉴스 검색
            news_items = fetch_naver_news(query, display=20)

            # 날짜 필터링 (사용자가 입력한 날짜에 해당하는 기사만 선택)
            filtered_news = []
            if date:
                for item in news_items:
                    pub_date = datetime.strptime(item["pubDate"], "%a, %d %b %Y %H:%M:%S %z")
                    if pub_date.date() == date.date():
                        filtered_news.append(item)
            else:
                filtered_news = news_items

            if not filtered_news:
                # st.warning("지정된 날짜나 쿼리에 맞는 뉴스가 없습니다.")
                st.session_state.messages.append({"role": "assistant", "content": "기사가 없습니다🥲"})
            else:
                # 뉴스 내용 전처리 및 벡터화
                documents = []
                summaries = []  # 요약 리스트
                sources = []  # 출처 리스트
                titles = []  # 제목 리스트
                dates = []  # 날짜 리스트

                for item in filtered_news:
                    # HTML 태그 제거
                    clean_article = clean_html(item["description"])
                    
                    raw_title = clean_html(item["title"])
                    clean_title = re.sub(r"\[.*?\]", "", raw_title).strip()

                    chunks = chunk_text(clean_article)
                    for chunk in chunks:
                        documents.append({"content": chunk, "source": item["originallink"]})
                    
                    # 요약
                    summaries.append(clean_html(item["description"]))

                    # 출처
                    sources.append(item["originallink"])

                    # 제목
                    titles.append(clean_title)

                    # 날짜
                    pub_date = datetime.strptime(item["pubDate"], "%a, %d %b %Y %H:%M:%S %z")
                    formatted_date = pub_date.strftime('%Y-%m-%d %p %I시')
                    formatted_date = formatted_date.replace('AM', '오전').replace('PM', '오후')
                    dates.append(formatted_date)

                texts = [doc["content"] for doc in documents]
                metadatas = [{"source": doc["source"]} for doc in documents]

                # Chroma 벡터스토어 생성, persist_directory 경로 설정
                vectorstore = Chroma.from_texts(
                    texts, 
                    embedding_model, 
                    persist_directory=persist_directory, 
                    metadatas=metadatas
                )
                retriever = vectorstore.as_retriever()

                # QA 체인 설정
                qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

                # 쿼리 처리
                result = qa_chain(query)
                answer = result["result"]

                # 챗봇 형식의 응답 출력
                st.session_state.messages.append({"role": "assistant", "content": answer})

                # 제목, 날짜, 요약, 출처 출력
                for title, summary, source, date in zip(titles, summaries, sources, dates):
                    combined_message = f"""
                    <div style="background-color:#FFFFFF; padding:15px; border-radius:10px; margin-bottom:20px; border:1px solid #ddd; width: 100%;">
                        <h5 style="color:#333; font-weight:bold; margin-bottom:10px; white-space: normal; word-wrap: break-word; overflow-wrap: break-word;">{title}</h5>
                        <p style="font-size:14px; color:#888; margin-bottom:10px;"><strong>날짜:</strong> {date}</p>
                        <p style="font-size:16px; color:#444; margin-bottom:15px;">{summary}</p>
                        <div style="text-align:right;">
                            <a href="{source}" target="_blank" style="display:inline-block; background-color:#FFBF00; color:white; padding:5px 15px; border-radius:5px; text-decoration:none;">🔗 원문 보기</a>
                        </div>
                    </div>
                    """

                    st.session_state.messages.append({"role": "assistant", "content": combined_message})

        except Exception as e:
            st.error(f"뉴스를 가져오는 중 오류가 발생했습니다: {e}")

# 전체 요약 출력
for msg in st.session_state.messages:
    if msg['role'] == 'assistant':
        st.markdown(msg['content'], unsafe_allow_html=True)
    else:
        st.chat_message(msg['role']).write(msg['content'])