import streamlit as st
import pandas as pd
from processor import process_excel, process_text, match_lists
from db import init_db, save_matched, load_matched, clear_db

init_db()

st.set_page_config(page_title="윌메이드 필터링 자동화", layout="wide")
st.title("📦 윌메이드 필터링 자동화 v2")


if "excel_df" not in st.session_state:
    st.session_state.excel_df = pd.DataFrame()
if "best_df" not in st.session_state:
    st.session_state.best_df = pd.DataFrame()

st.subheader("📁 1) 파일 업로드")

col1, col2 = st.columns(2)
with col1:
    excel_file = st.file_uploader("엑셀 파일 업로드 (xlsx)", type=["xlsx"])
with col2:
    best_file = st.file_uploader("최적 리스트 업로드 (txt, csv)", type=["txt", "csv"])

if st.button("🔍 필터링 실행"):
    if excel_file:
        st.session_state.excel_df = process_excel(excel_file)
    if best_file:
        st.session_state.best_df = process_text(best_file)

    matched_df = match_lists(st.session_state.excel_df, st.session_state.best_df)
    save_matched(matched_df)
    st.success("✔ 필터링 완료")


st.subheader("📚 2) 누적 리스트 관리")
left, right = st.columns(2)

with left:
    st.markdown("### 📂 엑셀 전체 누적 리스트")
    st.dataframe(st.session_state.excel_df, use_container_width=True)

with right:
    st.markdown("### 🎯 최적 매칭 누적 리스트")
    matched_db = load_matched()
    st.dataframe(matched_db, use_container_width=True)

if st.button("🗑 전체 데이터 초기화"):
    clear_db()
    st.warning("⚠ DB 초기화 완료")
