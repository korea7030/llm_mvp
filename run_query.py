from llm_project.langgraph_app import app
from llm_project.display_results import display_results


def run_query(user_input: str):
    result = app.invoke({"input": user_input})

    print('result : ', result)
    print("🔍 최종 결과:")
    layout_type = result.get("layout", "raw")
    hits = [(meta["user_name"], doc) for doc, meta in result["hits"]]
    query = result.get("query", "")

    # ✨ 하이라이트 단어 추출 (query를 단어 단위로 분리)
    highlight_terms = query.split() if query else []

    display_results(hits, layout_type=layout_type, highlight_terms=highlight_terms)
    # print("layout :", result["layout"])
    # for i, (doc, meta) in enumerate(result["hits"]):
    #     print(f"[{i}] {meta['timestamp']} {meta['user_name']}: {doc}")
    print("\n🔗 검색 방식:", result["search_type"])


if __name__ == '__main__':
    run_query("최민혁이 언급한 일본향에 대한 메시지를 보여줘")
    # run_query('2025년 1월 부터 4월까지 일본향에 대한 메시지를 보여줘')
    # run_query('gemini에 대한 메시지를 보여줘')
