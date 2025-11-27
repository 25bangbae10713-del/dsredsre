import streamlit as st
from datetime import datetime

st.set_page_config(page_title="FC Mobile 빠른 설명", page_icon="⚽", layout="wide")

# -----------------------------
# 기본 데이터
# -----------------------------
GAME_TITLE = "FC Mobile"
GAME_DESC = (
    "FC Mobile은 모바일에서 즐기는 축구 액션 & 팀 빌딩 게임입니다. "
    "선수 영입, 전술 설정, 경기 조작을 통해 실력을 키우는 게임입니다."
)

KEY_FEATURES = [
    ("팀 빌딩", "선수 영입, 성장, 포지션 배치"),
    ("전술 설정", "포메이션, 공격/수비 전략 조절"),
    ("실시간 경기", "터치 기반 슈팅, 패스, 드리블 조작"),
    ("이벤트/리그", "리그전, 친선전, 미션 이벤트"),
]

CONTROLS = {
    "터치 드리블": "드리블 및 방향 조절",
    "스와이프 슛": "슛 파워 조절 및 슛 방향 설정",
    "탭 패스": "빠르게 패스 진행",
    "스페셜 버튼": "특수 스킬 발동",
}

TIPS = [
    "초반에는 모든 포지션을 균형 있게 키우는 것이 좋습니다.",
    "상대 포메이션을 보고 공격 루트를 조절하세요.",
    "이벤트 보상은 선수 성장에 매우 중요합니다.",
]

GLOSSARY = {
    "포메이션": "선수 배치 형태 (예: 4-3-3, 4-2-3-1)",
    "스태미너": "선수의 체력, 경기 후반에 성능에 영향",
    "전술": "팀의 공격/수비 스타일",
}

EXAMPLE_PLAYERS = [
    {"name": "홍길동", "pos": "ST", "ovr": 78, "trait": "속력형"},
    {"name": "이민호", "pos": "CM", "ovr": 74, "trait": "패스마스터"},
    {"name": "김수아", "pos": "CB", "ovr": 76, "trait": "수비형"},
]

# -----------------------------
# UI 구성
# -----------------------------
st.title(f"{GAME_TITLE} — 빠른 설명 페이지 ⚽")

col1, col2 = st.columns([3, 1])

# 왼쪽 영역
with col1:
    st.header("게임 소개")
    st.write(GAME_DESC)

    st.header("핵심 기능")
    for name, desc in KEY_FEATURES:
        st.write(f"- **{name}**: {desc}")

    st.header("초보자 팁")
    for tip in TIPS:
        st.write(f"- {tip}")

    st.header("조작법")
    for key, value in CONTROLS.items():
        st.write(f"- **{key}**: {value}")

    st.header("예시 선수")
    for p in EXAMPLE_PLAYERS:
        st.write(f"{p['name']} — {p['pos']} | OVR {p['ovr']} | {p['trait']}")

    st.header("용어 모음")
    for term, meaning in GLOSSARY.items():
        st.write(f"- **{term}**: {meaning}")


# 오른쪽 사이드 영역
with col2:
    st.subheader("빠른 검색")
    search = st.text_input("검색어 입력", "")

    if search:
        st.write("검색 결과:")
        found = False

        # 용어 검색
        for term, meaning in GLOSSARY.items():
            if search.lower() in term.lower() or search.lower() in meaning.lower():
                st.write(f"- **{term}**: {meaning}")
                found = True

        # 기능 검색
        for name, desc in KEY_FEATURES:
            if search.lower() in name.lower() or search.lower() in desc.lower():
                st.write(f"- {name}: {desc}")
                found = True

        if not found:
            st.write("검색 결과가 없습니다.")

    st.subheader("텍스트 다운로드")
    text_data = (
        f"{GAME_TITLE}\n\n"
        f"{GAME_DESC}\n\n"
        "핵심 기능:\n" +
        "\n".join([f"- {n}: {d}" for n, d in KEY_FEATURES]) +
        "\n\n팁:\n" +
        "\n".join([f"- {t}" for t in TIPS])
    )

    st.download_button(
        "설명서 다운로드",
        text_data,
        file_name=f"fc_mobile_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
    )

# FAQ
st.markdown("---")
st.subheader("자주 묻는 질문")

faq = st.selectbox("질문을 선택하세요", [
    "골을 빨리 넣는 방법",
    "효율적인 선수 강화법",
    "초보자가 알아야 할 점",
])

if faq == "골을 빨리 넣는 방법":
    st.write("측면 공격, 스루 패스, 크로스 활용이 효과적입니다.")
elif faq == "효율적인 선수 강화법":
    st.write("이벤트 보상과 강화 재화를 모아 주전 선수부터 강화하세요.")
else:
    st.write("전술 변경과 조작법 숙지가 중요합니다. 초반 과금은 추천하지 않습니다.")

st.caption("이 페이지는 예시로 제작된 학습용 사이트입니다.")
