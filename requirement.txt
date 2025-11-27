import streamlit as st
from datetime import datetime
import os

# Try to import googletrans (community library) first. If not available, the app will
# fall back to requiring a Google Cloud Translate API key (recommended for reliability).
try:
    from googletrans import Translator, LANGUAGES as GT_LANGS
    HAS_GOOGLETRANS = True
except Exception:
    HAS_GOOGLETRANS = False
    GT_LANGS = {}

# A small helper to normalize language dictionaries into the form {code: name}
def get_language_map():
    # Primary source: googletrans languages if available
    lang_map = {}
    if HAS_GOOGLETRANS:
        # googletrans uses lowercase codes and English names
        for code, name in GT_LANGS.items():
            lang_map[code] = name.title()
    # Add some common extra aliases (optional)
    extras = {
        "auto": "Auto Detect",
    }
    for k, v in extras.items():
        if k not in lang_map:
            lang_map[k] = v
    # Make sure keys are sorted for display
    return dict(sorted(lang_map.items(), key=lambda x: x[1]))

LANG_MAP = get_language_map()

# Simple fuzzy search for language names or codes
def search_languages(query):
    q = query.strip().lower()
    if not q:
        return list(LANG_MAP.items())
    results = []
    for code, name in LANG_MAP.items():
        if q in code.lower() or q in name.lower():
            results.append((code, name))
    # if no direct substring matches, do a loose startswith / contains on tokens
    if not results:
        for code, name in LANG_MAP.items():
            tokens = name.lower().split()
            if any(t.startswith(q) for t in tokens):
                results.append((code, name))
    return results

# Translation function using googletrans if present
def translate_with_googletrans(text, src, dest):
    if not HAS_GOOGLETRANS:
        raise RuntimeError("googletrans 패키지가 설치되어 있지 않습니다.")
    translator = Translator()
    res = translator.translate(text, src=src if src != "auto" else None, dest=dest)
    return res.text, getattr(res, 'pronunciation', None)

# Placeholder for Google Cloud Translate fallback (requires API key)
def translate_with_google_cloud(text, src, dest, api_key):
    # We avoid depending on google-cloud-translate library here to keep the sample simple.
    # If you want to use Google Cloud Translate, install `google-cloud-translate` and
    # replace this function with an implementation that uses that client and the api_key.
    raise NotImplementedError("Google Cloud Translate fallback not implemented in this sample.\n"
                              "Install googletrans or implement the Cloud Translate client.")

# Streamlit UI
st.set_page_config(page_title="Universal Translator", page_icon="🌐", layout="wide")
st.title("세상의 모든 언어 번역기 — 유니버설 트랜슬레이터 🌍")
st.markdown(
    """
    이 앱은 `googletrans`(무료 커뮤니티 라이브러리)를 기본으로 사용합니다.

    **사용법**
    1. 왼쪽에서 번역할 언어(검색 가능)를 고르고, 번역될 언어를 선택하세요.
    2. 텍스트를 입력하고 `번역` 버튼을 누르세요.

    **주의**: `googletrans`는 비공식 라이브러리라 때때로 제한될 수 있습니다. 안정적 사용을 위해
    Google Cloud Translate API 키를 환경변수 `GOOGLE_API_KEY`로 설정하거나, 직접 Cloud Translate 클라이언트를
    연결하세요. (고급 옵션은 하단을 참고)
    """
)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("번역기")
    input_text = st.text_area("번역할 텍스트를 입력하세요", height=200)

    # Source language selector with search
    st.markdown("**원문 언어 (검색 가능)**")
    lang_search_src = st.text_input("원문 언어 검색", value="auto")
    src_options = search_languages(lang_search_src)
    # show as selectbox with "code — Name"
    src_choice = st.selectbox(
        "원문 언어 선택",
        options=[f"{code} — {name}" for code, name in src_options],
        index=0 if src_options else None,
    )
    src_code = src_choice.split(" — ")[0]

    # Target language selector with search
    st.markdown("**번역 언어 (검색 가능)**")
    lang_search_dst = st.text_input("번역 언어 검색", value="en", key="dst_search")
    dst_options = search_languages(lang_search_dst)
    dst_choice = st.selectbox(
        "번역 언어 선택",
        options=[f"{code} — {name}" for code, name in dst_options],
        index=0 if dst_options else None,
        key="dst_select",
    )
    dst_code = dst_choice.split(" — ")[0]

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        translate_btn = st.button("번역")
    with col_btn2:
        swap_btn = st.button("언어 바꾸기 ↔")

    if swap_btn:
        # Swap the search boxes by swapping their session state values
        tmp = st.session_state.get("dst_search", "en")
        st.session_state["dst_search"] = st.session_state.get("lang_search_src", "auto")
        st.session_state["lang_search_src"] = tmp
        st.experimental_rerun()

    translated_text = ""
    pronunciation = None

    if translate_btn:
        if not input_text.strip():
            st.warning("번역할 텍스트를 먼저 입력하세요.")
        else:
            try:
                if HAS_GOOGLETRANS:
                    translated_text, pronunciation = translate_with_googletrans(input_text, src_code, dst_code)
                else:
                    api_key = os.getenv("GOOGLE_API_KEY", None)
                    if api_key:
                        translated_text = translate_with_google_cloud(input_text, src_code, dst_code, api_key)
                    else:
                        st.error("서버에 `googletrans`가 설치되어 있지 않고, `GOOGLE_API_KEY`도 없습니다.\n"
                                 "googletrans를 설치하거나 Google Cloud Translate API 키를 설정하세요.")
            except Exception as e:
                st.error(f"번역 중 오류가 발생했습니다: {e}")

    if translated_text:
        st.subheader("번역 결과")
        st.write(translated_text)
        if pronunciation:
            st.caption(f"발음: {pronunciation}")
        # Download button
        st.download_button(
            "번역 결과 다운로드",
            translated_text,
            file_name=f"translation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
        )

with col2:
    st.subheader("언어 찾아보기 & 설명")
    q = st.text_input("언어 이름이나 코드를 입력해 찾아보세요 (예: korean, ko, spanish)")
    if q:
        matches = search_languages(q)
        if matches:
            for code, name in matches:
                st.write(f"**{code}** — {name}")
        else:
            st.write("일치하는 언어를 찾을 수 없습니다.")

    st.markdown("---")
    st.subheader("환경 설정 (옵션)")
    st.write("- 안정적이고 많은 언어 지원을 원하면 Google Cloud Translate API 키를 설정하세요.")
    st.write("- 기본 무료 옵션은 `googletrans` 라이브러리에 의존합니다 (비공식).\n  이를 사용하려면 레포에 requirements.txt에 `googletrans==4.0.0-rc1`를 추가하세요.")

    st.markdown("---")
    st.subheader("개발자용 메모")
    st.write(
        "이 샘플은 학습용입니다. '세상의 모든 언어'를 완벽히 지원하려면 상용 API(예: Google Cloud, Azure Translator, DeepL 엔터프라이즈 등)를 연결하는 것이 좋습니다."
    )

st.caption("이 앱은 예시용입니다. 실제 번역 품질은 사용된 엔진에 따라 달라집니다.")
