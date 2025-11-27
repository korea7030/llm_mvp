import json
import chromadb
from chromadb.config import Settings
from tqdm import tqdm

# 1. ChromaDB Persistent Client 설정
client = chromadb.PersistentClient(
    path="./chroma_store",  # 원하는 저장 경로로 변경 가능
    settings=Settings(anonymized_telemetry=False)
)
collection = client.get_or_create_collection("slack_messages")

# 2. 메시지 JSON 로딩
def load_messages_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# 3. 메시지를 ChromaDB에 저장
def add_messages_to_chroma(messages):
    for message in tqdm(messages, desc="Embedding Slack messages"):
        text = message.get("text", "").strip()
        if not text:
            continue

        doc_id = message.get("id")
        metadata = {
            "user_name": message.get("user_name", ""),
            "user_email": message.get("user_email", ""),
            "user_team": message.get("user_team", ""),
            "user_title": message.get("user_title", ""),
            "timestamp": message.get("timestamp", ""),
            "channel": message.get("channel", ""),
            "id": doc_id
        }

        try:
            collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[doc_id]
            )
        except Exception as e:
            print(f"❌ Error adding message {doc_id}: {e}")

# 4. 실행 진입점
if __name__ == "__main__":
    file_path = "./slack_messages_with_profiles.json"  # 저장된 원본 Slack 메시지 경로
    messages = load_messages_from_file(file_path)
    add_messages_to_chroma(messages)
    print("✅ ChromaDB 저장 완료!")