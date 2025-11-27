Fc Mobile Explainer Streamlit
· python
import streamlit as st


    st.header("예시 선수 스쿼드")
    for p in EXAMPLE_PLAYERS:
        st.write(f"{p['name']} — {p['pos']} • OVR {p['ovr']} • {p['trait']}")


    with st.expander("전술 템플릿 예시 (클릭하여 보기)"):
        st.subheader("안정형 4-2-3-1")
        st.write("수비를 안정시키고 역습에 강한 설정. 수비형 미드필더 2명을 둡니다.")
        st.subheader("공격형 4-3-3")
        st.write("전방 압박과 측면 공격을 활용하는 공격적인 템플릿입니다.")


    st.header("용어집")
    for term, meaning in GLOSSARY.items():
        st.write(f"**{term}** — {meaning}")


with col2:
    st.info("사이드바: 빠른 검색 & 설명 복사")


    search_term = st.text_input("찾을 용어 검색", "포메이션")
    if search_term:
        results = []
        # 간단한 검색: 키, 키워드 포함 여부
        for d in [GAME_DESC] + [f"{name}: {desc}" for name, desc in KEY_FEATURES]:
            if search_term.lower() in d.lower():
                results.append(d)
        for term, meaning in GLOSSARY.items():
            if search_term.lower() in term.lower() or search_term.lower() in meaning.lower():
                results.append(f"{term} — {meaning}")
        if results:
            st.write("검색 결과:")
            for r in results:
                st.write("- ", r)
        else:
            st.write("검색 결과가 없습니다. 다른 단어로 시도하세요.")


    st.download_button(
        label="설명서 텍스트로 다운로드",
        data="\n".join([
            GAME_TITLE,
            "",
            GAME_DESC,
            "",
            "핵심 기능:",
        ] + [f"- {n}: {d}" for n, d in KEY_FEATURES] + ["", "팁:"] + [f"- {t}" for t in TIPS]),
        file_name=f"{GAME_TITLE}_cheatsheet_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
    )


# Footer: 간단한 Q&A 자동 생성
st.markdown("---")
st.subheader("자주 묻는 질문(자동 생성)")
faq_q = st.selectbox("질문 선택", [
    "경기에서 빠르게 점수를 올리는 방법",
    "선수 레벨업 효율적으로 하는 법",
    "초보자가 주의할 점",
])


if faq_q == "경기에서 빠르게 점수를 올리는 방법":
    st.write("측면 돌파 후 크로스, 세트피스 기회를 노려보세요. 직접 슛을 노릴 때는 슛 파워와 정확도를 함께 고려하세요.")
elif faq_q == "선수 레벨업 효율적으로 하는 법":
    st.write("주전 선수 위주로 훈련 횟수를 투자하고, 이벤트 보상으로 얻는 경험치 버프를 활용하세요.")
else:
    st.write("초반에는 무리한 과금이나 선수 편중을 피하고, 게임의 기본 조작과 전술 변화를 익히세요.")


# Small utility: Export current page content as markdown
if st.button("페이지 내용 복사(마크다운) → 클립보드"):
    md = []
    md.append(f"# {GAME_TITLE}\n")
    md.append(GAME_DESC + "\n")
    md.append("## 핵심 기능\n")
    for n, d in KEY_FEATURES:
        md.append(f"- **{n}**: {d}\n")
    st.code("\n".join(md))
    st.success("마크다운 형식이 아래 코드 블록에 생성되었습니다. Ctrl+C로 복사하세요.")


# 마지막 안내
st.caption("이 앱은 학습용 예시입니다. 실제 게임 정보는 게임 내 가이드나 공식 페이지를 참고하세요.")
