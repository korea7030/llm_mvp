# search_chroma.py

from llm_project.hybrid_search import hybrid_search
import chromadb

client = chromadb.PersistentClient(path="./chroma_store")
collection = client.get_or_create_collection("slack_messages")

def search_chroma(state: dict) -> dict:
    parsed = state["parsed_query"]
    query = parsed.get("query", "")
    user_name = parsed.get("user_name")
    start_date = parsed.get("start_date")
    end_date = parsed.get("end_date")

    print(f"[DEBUG] Hybrid Search Query: {query}")
    print(f"[DEBUG] Filters - user_name: {user_name}, date: {start_date} ~ {end_date}")

    hits = hybrid_search(
        collection,
        query=query,
        user_name=user_name,
        start_date=start_date,
        end_date=end_date,
        strict=True
    )
    print('hybrid :: ', hits)

    return {
        "hits": hits,
        "search_type": "hybrid",
        "parsed_query": parsed,
    }