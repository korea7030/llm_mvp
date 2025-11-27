from datetime import datetime
from markupsafe import escape
from typing import List, Tuple, Dict
from tabulate import tabulate

def highlight(text: str, terms: List[str]) -> str:
    for term in terms:
        text = text.replace(term, f"\033[93m{term}\033[0m")  # yellow
    return text

def display_results(hits: List[tuple], layout_type="table", highlight_terms=None):
    if not hits:
        return "<p class='text-red-500'>❌ 관련 메시지를 찾을 수 없습니다.</p>"

    # 정렬: 채널, 타임스탬프 순
    def parse_ts(ts):
        try:
            # print('!!!!! : ', datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M"))
            formatted_ts = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M")
            return formatted_ts
        except:
            return datetime.min

    hits.sort(key=lambda h: (h[2], parse_ts(h[1])))  # channel, timestamp

    def highlight(text: str) -> str:
        for term in highlight_terms or []:
            text = text.replace(term, f"<mark class='bg-yellow-200 px-1 rounded'>{escape(term)}</mark>")
        return text

    # 🎨 Tailwind 스타일 테이블
    if layout_type == "table":
        html = """
        <div class="overflow-x-auto">
        <table class="table-auto w-full border border-gray-300 text-sm">
            <thead class="bg-gray-100 text-left">
                <tr>
                    <th class="px-4 py-2 border">채널</th>
                    <th class="px-4 py-2 border">시간</th>
                    <th class="px-4 py-2 border">사용자</th>
                    <th class="px-4 py-2 border">메시지</th>
                </tr>
            </thead>
            <tbody>
        """
        for user_name, timestamp, channel, message in hits:
            try:
                formatted_ts = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M")
            except:
                formatted_ts = timestamp  # 포맷 안 맞으면 fallback

            html += f"""
            <tr class="hover:bg-gray-50">
                <td class="px-4 py-2 border">{escape(channel)}</td>
                <td class="px-4 py-2 border">{escape(formatted_ts)}</td>
                <td class="px-4 py-2 border">{escape(user_name)}</td>
                <td class="px-4 py-2 border">{highlight(message)}</td>
            </tr>
            """
        html += "</tbody></table></div>"
        return html

    # 🎨 Tailwind 스타일 아코디언
    elif layout_type == "accordion":
        html = """
        <div class="space-y-2">
        """
        for user_name, timestamp, channel, message in hits:
            try:
                formatted_ts = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M")
            except:
                formatted_ts = timestamp  # 포맷 안 맞으면 fallback

            header = f"{user_name} ({channel} / {formatted_ts})"
            html += f"""
            <div class="border border-gray-300 rounded-lg">
                <button class="accordion-toggle w-full text-left px-4 py-2 bg-gray-100 font-semibold">
                    💬 {escape(header)}
                </button>
                <div class="accordion-content hidden px-4 py-2 bg-white text-sm">
                    {highlight(message)}
                </div>
            </div>
            """
        html += "</div>"

        # ✅ DOMContentLoaded 감싸기
        html += """
        <script>
        document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".accordion-toggle").forEach(button => {
            button.addEventListener("click", () => {
            const content = button.nextElementSibling;
            content.classList.toggle("hidden");
            });
        });
        });
        </script>
        """
        return html

    # 🔁 기본: 단순 리스트
    else:
        return "<br>".join([
            f"<b>{escape(user_name)}</b> ({escape(channel)} / {escape(datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M'))}): {highlight(message)}"
            for user_name, timestamp, channel, message in hits
        ])
# def display_results(hits: List[Dict], layout_type="table", highlight_terms=None):
#     from markupsafe import escape
#     from datetime import datetime

#     if not hits:
#         return "<p>❌ 관련 메시지를 찾을 수 없습니다.</p>"

#     # Step 1: 채널별 + 시간순 정렬
#     def parse_ts(ts):
#         try:
#             return datetime.fromisoformat(ts)
#         except:
#             return datetime.min

#     # ✅ 정렬 시 KeyError, AttributeError 방지
#     hits.sort(key=lambda h: (h[2], parse_ts(h[1])))  # channel, timestamp
#     # hits.sort(key=lambda h: (
#     #     h.get("channel", ""), 
#     #     parse_ts(h.get("timestamp", ""))
#     # ))

#     # Step 2: 하이라이팅 함수
#     def highlight(text):
#         for term in highlight_terms or []:
#             text = text.replace(term, f"<mark>{escape(term)}</mark>")
#         return text

#     # Step 3: 렌더링
#     if layout_type == "table":
#         html = "<table><tr><th>채널</th><th>시간</th><th>사용자</th><th>메시지</th></tr>"
#         for h in hits:
#             html += f"<tr><td>{escape(h[2])}</td><td>{escape(h[1])}</td><td>{escape(h[0])}</td><td>{highlight(h[3])}</td></tr>"
#         html += "</table>"
#         return html

#     elif layout_type == "accordion":
#         html = "<div class='accordion'>"
#         for h in hits:
#             header = f"💬 {h[0]} ({h[2]} / {h[1]})"
#             html += f"""
#             <button class="accordion-btn">{escape(header)}</button>
#             <div class="accordion-content">{highlight(h[3])}</div>
#             """
#         html += "</div>"
#         return html

#     else:
#         return "<br>".join([
#             f"<b>{escape(h[0])}</b> ({escape(h[2])} / {escape(h[1])}): {highlight(h[3])}"
#             for h in hits
#         ])
