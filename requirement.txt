import streamlit as st
from datetime import datetime

st.set_page_config(page_title="FC Mobile 스쿼드 & 공략 (수익화 버전)", page_icon="💰", layout="wide")

# -----------------------
# 1️⃣ 홈 & 소개
# -----------------------
st.title("⚽ FC Mobile 스쿼드 추천 & 공략 사이트 💰")
st.markdown("""
이 사이트는 **FC Mobile 스쿼드 추천 + 공략 정보**를 제공하며,  
후원과 광고를 통해 개발자를 지원할 수 있습니다.
- 스쿼드 추천 & 선수 검색  
- 초보/중급자 공략 정보  
- PDF 다운로드 기능(후원 시 가능)
""")

st.markdown("---")

# -----------------------
# 2️⃣ 스쿼드 추천
# -----------------------
st.header("🏟️ 스쿼드 추천")
players = [
    {"name": "홍길동", "pos": "ST", "ovr": 78, "trait": "속력형"},
    {"name": "이민호", "pos": "CM", "ovr": 74, "trait": "패스마스터"},
    {"name": "김수아", "pos": "CB", "ovr": 76, "trait": "수비형"},
    {"name": "박지훈", "pos": "LW", "ovr": 72, "trait": "드리블형"},
    {"name": "최윤서", "pos": "RW", "ovr": 73, "trait": "스피드형"},
    {"name": "강하늘", "pos": "GK", "ovr": 80, "trait": "골키퍼 전문가"},
]

formation = st.selectbox("포메이션 선택", ["4-3-3", "4-2-3-1", "3-5-2"])
st.subheader(f"{formation} 추천 스쿼드")
st.table(players)

st.markdown("---")

# -----------------------
# 3️⃣ 공략 정보
# -----------------------
st.header("📖 공략 정보")
guides = [
    "초반에는 전체 포지션 균형 있게 성장시키기",
    "상대 팀 포메이션에 맞춘 공격 루트 조절",
    "중반 이후 스페셜 스킬 활용 극대화",
    "이벤트 참여로 보상 및 경험치 확보",
    "골키퍼와 수비진은 체력 관리 필수"
]
for idx, tip in enumerate(guides, 1):
    st.write(f"{idx}. {tip}")

st.markdown("---")

# -----------------------
# 4️⃣ 선수 검색 & 추천
# -----------------------
st.header("🔍 선수 검색 & 추천")
search_name = st.text_input("선수 이름 검색", "")
if search_name:
    results = [p for p in players if search_name.lower() in p['name'].lower()]
    if results:
        st.write("검색 결과:")
        st.table(results)
    else:
        st.write("검색 결과가 없습니다.")

pos_choice = st.selectbox("포지션별 추천 선수 보기", ["ST","CM","CB","LW","RW","GK"])
recommended = [p for p in players if p['pos'] == pos_choice]
st.subheader(f"{pos_choice} 포지션 추천 선수")
st.table(recommended)

st.markdown("---")

# -----------------------
# 5️⃣ PDF 다운로드 (후원 기반)
# -----------------------
st.header("💾 PDF 다운로드 (후원 필요)")
st.write("후원 시 스쿼드 + 공략 PDF를 다운로드할 수 있습니다.")

# 후원 링크 예제 (토스, 페이팔 등)
st.markdown("""
[💰 후원하기 - 토스](https://toss.me/)  
[💰 후원하기 - PayPal](https://www.paypal.com/donate)
""")

if st.button("PDF 다운로드 시뮬레이션"):
    st.success("후원 후 PDF 다운로드가 가능합니다! (실제 결제 연동 필요)")
    text_data = f"""
FC Mobile 스쿼드 추천 & 공략
작성일: {datetime.now().strftime('%Y-%m-%d')}

포메이션: {formation}

추천 스쿼드:
"""
    for p in players:
        text_data += f"- {p['name']} | {p['pos']} | OVR {p['ovr']} | {p['trait']}\n"
    text_data += "\n공략 정보:\n"
    for tip in guides:
        text_data += f"- {tip}\n"
    st.download_button(
        "다운로드 PDF(텍스트)", text_data,
        file_name=f"fc_mobile_guide_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

st.markdown("---")

# -----------------------
# 6️⃣ 광고 배너 예제
# -----------------------
st.header("📢 광고 배너")
st.info("여기에 실제 Google AdSense 광고 코드 삽입 가능")
st.markdown("""
[광고 영역 예시]  
- 게임 용품, 스마트폰, 구글 플레이 게임 추천 등
""")

st.markdown("---")

# -----------------------
# 7️⃣ 사용자 통계 기록 (간단)
# -----------------------
st.header("📊 간단 통계 (클릭/다운로드)")
if 'downloads' not in st.session_state:
    st.session_state.downloads = 0
if st.button("다운로드 기록 추가"):
    st.session_state.downloads += 1
st.write(f"총 PDF 다운로드 시뮬레이션 횟수: {st.session_state.downloads}")

st.caption("⚠️ 실제 수익화 시에는 결제 API 연동, 광고 스크립트 삽입 필요")
