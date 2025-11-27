# Slack 메시지 검색 시스템 (llm_mvp)

[GitHub Repository](https://github.com/korea7030/llm_mvp)

## 📌 프로젝트 개요  
Slack 메시지를 자연어 쿼리로 검색하고, 결과를 가독성 있게 보여주는 웹 애플리케이션입니다.  
예: “정지성이 언급한 gemini 메시지” 같은 문장 입력 → 해당 조건에 맞는 Slack 메시지 검색 & 표시.

## 🧑‍💻 주요 역할  
- Python + Flask 기반 백엔드 서버 구축  
- 자연어 쿼리 파싱 및 사용자 이름 / 날짜 / 키워드 추출 로직 구현  
- 검색 로직 + 필터 + fallback 처리  
- UI 설계 및 프론트엔드 구현 (HTML + Tailwind CSS + Vanilla JS)  
- 결과 레이아웃: 테이블 / 아코디언(toggle) 형태 지원  
- 키워드 하이라이팅, 결과 정렬 (채널 / 시간 기준) 기능 구현  

## ⚙️ 사용 기술 & 라이브러리  
| 영역 | 기술 / 라이브러리 |
|------|------------------|
| Backend | Python 3.11, Flask, Jinja2 |
| Frontend | HTML, Tailwind CSS, Vanilla JavaScript |
| 데이터 | JSON (Slack 메시지 로그) |
| 유틸리티 | datetime, Markupsafe 등 |

## 💡 기능 요약

- ✅ 자연어 기반 검색: 자유로운 문장 입력 → 해당 조건 해석 + 검색  
- ✅ 필터링: 사용자 이름, 날짜 범위 등 조건 필터링 가능  
- ✅ 레이아웃 선택:  
  - 테이블(Table)  
  - 아코디언(Accordion) — 클릭 시 메시지 열기/닫기  
- ✅ 검색어 하이라이팅: 키워드가 포함된 부분을 `<mark>` 태그로 강조  
- ✅ 정렬: 채널 이름, 타임스탬프 순으로 정렬  
- ✅ 반응형 UI + 간결한 스타일링 (Tailwind 사용)  

## 🔧 설치 / 실행 방법  

```bash
# 저장소 클론
git clone https://github.com/korea7030/llm_mvp.git
cd llm_mvp

# (선택) 가상환경 생성 & 활성화
python -m venv .venv
source .venv/bin/activate  # Mac / Linux
# .venv\\Scripts\\activate   # Windows

# 필요한 패키지 설치
pip install flask markupsafe  # + 기타 필요 라이브러리

# 서버 실행
python app.py  # 또는 프로젝트에서 설정한 진입점