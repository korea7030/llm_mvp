from langgraph.graph import StateGraph, END
from typing import Dict
from llm_project.parse_query import parse_query
from llm_project.search_chroma import search_chroma
from llm_project.render_result import render_result


# ---------------------------
# 상태 정의
# ---------------------------
State = Dict[str, object]


# ---------------------------
# LangGraph 구성
# ---------------------------
workflow = StateGraph(State)

# Step 1: 자연어 파싱 → structured query
workflow.add_node("parse_query", parse_query)

# Step 2: Chroma 검색
workflow.add_node("search_chroma", search_chroma)

# Step 3: 결과 렌더링
workflow.add_node("render_result", render_result)

# 노드 연결
workflow.set_entry_point("parse_query")
workflow.add_edge("parse_query", "search_chroma")
workflow.add_edge("search_chroma", "render_result")
workflow.set_finish_point("render_result")

# 컴파일된 그래프 생성
app = workflow.compile()

