# parse_layout.py
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
import json

# LLM 설정
llm = OllamaLLM(model="mistral")

# 프롬프트 정의
layout_prompt = PromptTemplate.from_template("""
다음 사용자의 검색 질의에 가장 적합한 UI 레이아웃을 선택하고 JSON으로 출력하세요.

가능한 layout_type 값: "table", "accordion", "chart", "timeline", "raw"

형식:
{{
  "layout_type": "table | accordion | chart | timeline | raw",
  "group_by": "user_name | team | date | null",
  "highlight_terms": ["단어1", "단어2"]
}}

사용자 입력:
"{input}"

출력:
JSON 형식으로만 출력하세요. 설명은 생략하세요.
""")

# 체인 연결
layout_chain = layout_prompt | llm | StrOutputParser()

# LangGraph-compatible node
def parse_layout(state: dict) -> dict:
    user_input = state["input"]
    try:
        response = layout_chain.invoke({"input": user_input})
        layout = json.loads(response)
        print("[DEBUG] layout_spec:", layout)  # ✅ 이 부분 추가
        return {"layout_spec": layout}
    except Exception as e:
        print(f"[❌ parse_layout error] {e}")
        return {"layout_spec": {"layout_type": "raw", "group_by": None, "highlight_terms": []}}