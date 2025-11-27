from typing import Dict, List, Tuple


def render_result(state: Dict) -> Dict:
    """
    검색 결과(state["hits"])를 사람이 보기 좋은 형식으로 정리합니다.
    hits: List of (document, metadata)
    """
    hits: List[Tuple[str, Dict]] = state.get("hits", [])
    query: str = state.get("parsed_query", {}).get("query", "")
    search_type: str = state.get("search_type", "unknown")

    # 결과가 없으면 fallback 메시지 제공
    if not hits:
        return {
            "layout": "empty",
            "query": query,
            "hits": [],
            "search_type": search_type,
            "message": "❌ 관련된 메시지를 찾을 수 없습니다."
        }

    # LLM이 추천한 layout_spec을 우선 반영
    layout_spec = state.get("parsed_query", {}).get("layout_spec", "").lower()

    if layout_spec in ["table", "summary", "요약"]:
        layout = "table"
    elif layout_spec in ["accordion", "raw", "원문"]:
        layout = "accordion"
    else:
        # fallback: 결과 수에 따라 결정
        layout = "accordion" if len(hits) > 5 else "table"

    return {
        "layout": layout,
        "query": query,
        "hits": hits,
        "search_type": search_type
    }