import pathlib
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="QuickQuote - 해외 영업 견적서 자동 생성기",
    layout="wide",
)

HTML_PATH = pathlib.Path(__file__).parent / "index.html"
html_code = HTML_PATH.read_text(encoding="utf-8")

# 견적 항목이 늘어나거나 미리보기가 길어져도 잘리지 않도록
# 높이를 넉넉히 잡고 내부 스크롤을 허용합니다.
components.html(html_code, height=1600, scrolling=True)
