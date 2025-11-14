import streamlit as st
import pandas as pd
from processor import update_master   # load_master 제거

st.set_page_config(page_title="윌메이드 필터링 자동화", layout="wide")

st.title("📦 윌메이드 필터링 자동화")

st.subheader("📁 1) 파일 업로드")

uploaded_excel = st.file_uploader("엑셀 파일 업로드 (xlsx)", type=["xlsx"])
uploaded_optimal = st.file_uploader("최적 리스트 업로드 (txt, csv)", type=["txt", "csv"])

if st.button("필터링 실행"):
    if uploaded_excel is None or uploaded_optimal is None:
        st.error("두 개의 파일 모두 업로드 해주세요.")
    else:
        excel_df = pd.read_excel(uploaded_excel)
        optimal_df = pd.read_csv(uploaded_optimal, header=None, names=["블로그ID"])

        master_df, today_excel_df, selected_df = update_master(excel_df, optimal_df)

        st.success("필터링 완료 ✔")

        # --- 화면 2분할 표시 ---
        left, right = st.columns(2)

        with left:
            st.subheader("📊 오늘 업로드된 엑셀 결과")
            st.dataframe(today_excel_df, use_container_width=True)

        with right:
            st.subheader("📌 최종 누적 리스트 (중복 제거 자동)")
            st.dataframe(master_df, use_container_width=True)
