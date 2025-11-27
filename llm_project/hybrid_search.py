# hybrid_search.py

from datetime import date

def hybrid_search(collection, query, user_name=None, start_date=None, end_date=None, strict=True):
    """
    ChromaDB 유사도 검색 + 키워드 포함 여부 직접 필터링 (하이브리드 방식)
    """
    query_lower = query.lower()
    keyword_hits = []
    similarity_hits = []

    # Step 1: 유사도 검색
    filters = {"user_name": {"$eq": user_name}} if user_name else {}
    try:
        result = collection.query(
            query_texts=[query],
            # n_results=20,
            where=filters or None,
            include=["documents", "metadatas"]
        )
    except Exception as e:
        print("❌ Chroma similarity search failed:", e)
        return []

    for doc, meta in zip(result["documents"][0], result["metadatas"][0]):
        if user_name:
            meta_name = meta.get("user_name", "")
            print(meta_name)
            if user_name not in meta_name:
                continue

        if start_date and end_date:
            try:
                ts = date.fromisoformat(meta.get("timestamp", "")[:10])
                if not (date.fromisoformat(start_date) <= ts <= date.fromisoformat(end_date)):
                    continue
            except:
                continue
        if query_lower in doc.lower():
            keyword_hits.append((doc, meta))
        else:
            similarity_hits.append((doc, meta))

    # Step 2: 키워드 직접 포함 확인 (fallback)
    try:
        all_docs = collection.get(include=["documents", "metadatas"])
    except Exception as e:
        print("❌ Chroma fallback keyword search failed:", e)
        return keyword_hits + similarity_hits

    for doc, meta in zip(all_docs["documents"], all_docs["metadatas"]):
        if query_lower not in doc.lower():
            continue

        if user_name:
            meta_name = meta.get("user_name", "")
            if user_name not in meta_name:
                continue

        if start_date and end_date:
            try:
                ts = date.fromisoformat(meta.get("timestamp", "")[:10])
                if not (date.fromisoformat(start_date) <= ts <= date.fromisoformat(end_date)):
                    continue
            except:
                continue

        keyword_hits.append((doc, meta))
        # if query_lower in doc.lower():
        #     if start_date and end_date:
        #         try:
        #             ts = date.fromisoformat(meta.get("timestamp", "")[:10])
        #             if not (date.fromisoformat(start_date) <= ts <= date.fromisoformat(end_date)):
        #                 continue
        #         except:
        #             continue

        #     keyword_hits.append((doc, meta))

    # print(keyword_hits)
    # print(similarity_hits)
    # Step 3: 중복 제거 + 병합
    seen = set()
    final_hits = []
    for doc, meta in keyword_hits + similarity_hits:
        if doc not in seen:
            # final_hits.append((doc, meta))
            final_hits.append((doc, meta))
            seen.add(doc)

    return final_hits if not strict else keyword_hits