# # 전체 메시지에서 gemini 포함된 것만 필터
# from chromadb import PersistentClient

# client = PersistentClient(path="./chroma_store")
# collection = client.get_collection("slack_messages")

# all_docs = collection.get(include=["documents", "metadatas"])
# docs = all_docs["documents"]
# metas = all_docs["metadatas"]

# print("🔍 Gemini 키워드 포함 메시지:")
# found = 0
# for doc, meta in zip(docs, metas):
#     if "gemini" in doc.lower():
#         found += 1
#         print(f"\n👤 {meta.get('user_name', '')}\n📄 {doc}")

# if found == 0:
#     print("❌ 'Gemini' 키워드가 포함된 메시지가 없습니다.")
# else:
#     print(f"\n✅ 총 {found}건의 메시지에서 'Gemini'가 발견되었습니다.")

from chromadb.config import Settings
import chromadb

client = chromadb.PersistentClient(path="./chroma_store")
collection = client.get_or_create_collection("slack_messages")

# 모든 문서에서 user_name과 함께 출력
all = collection.get(include=["metadatas", "documents"])

print("📌 저장된 유저들:")
print(set([meta["user_name"] for meta in all["metadatas"]]))

print("📌 Gemini 포함 메시지 여부 확인:")
for meta, doc in zip(all["metadatas"], all["documents"]):
    if "gemini" in doc.lower():
        print(f"✅ {meta['user_name']}: {doc}")