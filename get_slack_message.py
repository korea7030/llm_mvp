import re

import hashlib
import time
import json
from slack_sdk import WebClient
from datetime import datetime

client = WebClient(token='xxx')  # token : 원하는 토크능로 설정

# 날짜 변환
def ts_to_iso(ts: str) -> str:
    return datetime.fromtimestamp(float(ts)).isoformat()

# 사용자 정보 캐싱
user_info_cache = {}

def get_user_info(user_id):
    if user_id in user_info_cache:
        return user_info_cache[user_id]

    try:
        user_resp = client.users_info(user=user_id)
        profile = user_resp['user']['profile']
        team = ""
        # 사용자 정의 필드에서 팀명 추출
        fields = profile.get("fields", {})
        for field_id, field in (fields or {}).items():
            label = field.get("label", "").lower()
            if "team" in label:
                team = field.get("value", "")
                break

        info = {
            "name": profile.get("display_name", ""),
            "email": profile.get("email", ""),
            "team": team,
            "title": profile.get("title", ""),
        }
        user_info_cache[user_id] = info
        return info

    except Exception as e:
        print(f"⚠️ 사용자 정보 가져오기 실패: {user_id} - {e}")
        return {
            "name": "Unknown",
            "email": "",
            "team": "",
            "title": ""
        }

# ✅ 멘션 치환 함수: <@U123ABC> → @이름
mention_pattern = re.compile(r"<@([UW][A-Z0-9]+)>")

def replace_mentions(text):
    def replace_match(match):
        user_id = match.group(1)
        user_info = get_user_info(user_id)
        return f"@{user_info['name']}" if user_info else match.group(0)
    return mention_pattern.sub(replace_match, text)

# 📥 메시지 수집
messages_data = []
seen_ids = set()

response = client.conversations_list(types="public_channel,private_channel,im,mpim")
channels = response["channels"]

for channel in channels:
    cid = channel["id"]
    cname = channel.get("name") or f"DM_{channel.get('user')}"

    try:
        history = client.conversations_history(channel=cid, limit=200)
    except Exception as e:
        print(f"❌ {cname} 메시지 수집 실패: {e}")
        continue

    for msg in history["messages"]:
        try:
            uid = msg.get('user', 'unknown')
            ts = msg['ts']
            text = msg.get('text', '')
            text = replace_mentions(text)  # ✅ 멘션 치환

            # 🔑 유니크 ID 생성
            raw_id = f"{cname}_{ts}_{uid}_{text}"
            unique_id = f"{cname}_{ts}_{uid}_{hashlib.md5(raw_id.encode()).hexdigest()[:8]}"
            if unique_id in seen_ids:
                continue
            seen_ids.add(unique_id)

            user_info = get_user_info(uid)

            user_title = user_info['title'].strip()
            team = ''
            title = ''

            # 팀/직책 파싱
            match = re.match(r"^(.*?)\s*【(.*?)】$", user_title)
            if match:
                team = match.group(1).strip()
                title = match.group(2).strip()
            match = re.match(r"^(.*?)\s*\[(.*?)\]$", user_title)
            if match:
                team = match.group(1).strip()
                title = match.group(2).strip()

            msg_obj = {
                "id": unique_id,
                "channel": cname,
                "user": uid,
                "timestamp": ts_to_iso(ts),
                "text": text,
                "is_thread": False,
                "user_name": user_info["name"],
                "user_email": user_info["email"],
                "user_team": team,
                "user_title": title
            }
            messages_data.append(msg_obj)

            # 🧵 스레드 수집
            if "thread_ts" in msg:
                time.sleep(1.2)
                thread = client.conversations_replies(channel=cid, ts=msg["thread_ts"])
                for tmsg in thread["messages"][1:]:
                    t_uid = tmsg.get('user', 'unknown')
                    t_ts = tmsg['ts']
                    t_text = tmsg.get('text', '')
                    t_text = replace_mentions(t_text)  # ✅ 멘션 치환

                    t_raw_id = f"{cname}_{t_ts}_{t_uid}_{t_text}"
                    t_unique_id = f"{cname}_{t_ts}_{t_uid}_{hashlib.md5(t_raw_id.encode()).hexdigest()[:8]}"
                    if t_unique_id in seen_ids:
                        continue
                    seen_ids.add(t_unique_id)

                    t_user_info = get_user_info(t_uid)

                    tmsg_obj = {
                        "id": t_unique_id,
                        "channel": cname,
                        "user": t_uid,
                        "timestamp": ts_to_iso(t_ts),
                        "text": t_text,
                        "is_thread": True,
                        "user_name": t_user_info["name"],
                        "user_email": t_user_info["email"],
                        "user_team": t_user_info["team"],
                        "user_title": t_user_info["title"]
                    }
                    messages_data.append(tmsg_obj)

        except Exception as e:
            print(f"⚠️ 에러: {e}")
            continue

# 💾 저장
with open("slack_messages_with_profiles.json", "w", encoding="utf-8") as f:
    json.dump(messages_data, f, indent=2, ensure_ascii=False)

print(f"✅ 총 저장된 메시지: {len(messages_data)}개")