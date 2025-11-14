import streamlit as st
import pandas as pd
from processor import update_master, load_master

st.set_page_config(page_title="윌메이드 필터링 자동화", layout="wide")

if "master_df" not in st.session_state:
    st.session_state.master_df = load_master()

st.title("📦 윌메이드 필터링 자동화")

uploaded_excel = st.file_uploader("엑셀 파일 업로드 (xlsx)", type=["xlsx"])
uploaded_optimal = st.file_uploader("최적 리스트 업로드 (txt, csv)", type=["txt", "csv"])

if st.button("필터링 실행"):
    if uploaded_excel is None or uploaded_optimal is None:
        st.error("두 개 파일 업로드해주세요.")
    else:
        excel_df = pd.read_excel(uploaded_excel)
        optimal_df = pd.read_csv(uploaded_optimal, header=None, names=["아이디"])
        st.session_state.master_df, today_df, extracted_df = update_master(excel_df, optimal_df)

        st.success("필터링 완료")
        st.dataframe(today_df)
        st.dataframe(st.session_state.master_df)
