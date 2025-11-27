# parse_query.py
from typing import Dict
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
import json
import re

llm = OllamaLLM(model="mistral")

prompt = PromptTemplate.from_template("""
다음은 슬랙 대화 검색 시스템에서 사용하는 쿼리입니다.
자연어로 된 사용자의 입력을 아래 JSON 형식으로 변환하세요.

형식:
{{
  "query": "검색할 핵심 키워드",
  "user_name": "특정 사용자가 언급된 경우 이름만 추출 없으면 null",
  "user_team": "언급된 팀명, 없으면 null",
  "start_date": "YYYY-MM-DD 형식 (있으면)",
  "end_date": "YYYY-MM-DD 형식 (있으면)"
}}

입력:
"{input}"

출력 JSON만 제공하세요.
""")

chain = prompt | llm | StrOutputParser()

# ✨ Fallback 사용자 이름 추출 (ex. "정지성님" → "정지성")
def extract_name_from_query_text(query_text: str) -> str | None:
    match = re.search(r"([가-힣]{2,4})(님|이|의|가)?\s*(이( 작성한| 보낸| 작성된| 작성)?|가 작성한)?", query_text)
    if match:
        return match.group(1)
    return None

# LangGraph 노드 함수
def parse_query(state: Dict) -> Dict:
    user_input = state["input"]
    try:
        response = chain.invoke({"input": user_input})
        parsed = json.loads(response)

        # Fallback: user_name이 None이면 query에서 추출
        # if not parsed.get("user_name"):
        #     fallback_name = extract_name_from_query_text(parsed.get("query", ""))
        #     parsed["user_name"] = fallback_name
        #     print(f"⚠️ Fallback 추출된 사용자 이름: {fallback_name}")

        return {"parsed_query": parsed}

    except Exception as e:
        print(f"❌ Parse Error: {e}")
        return {"parsed_query": {"query": user_input, "user_name": None}}