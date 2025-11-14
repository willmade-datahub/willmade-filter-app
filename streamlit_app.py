import streamlit as st
import pandas as pd
from processor import update_master

st.set_page_config(page_title="윌메이드 필터링 자동화", layout="wide")

if "master_df" not in st.session_state:
    st.session_state.master_df = None
if "excel_df" not in st.session_state:
    st.session_state.excel_df = None

st.title("📦 윌메이드 필터링 자동화")

uploaded_excel = st.file_uploader("엑셀 파일 업로드 (xlsx)", type=["xlsx"])
uploaded_optimal = st.file_uploader("최적 리스트 업로드 (txt, csv)", type=["txt", "csv"])

if st.button("필터링 실행"):
    excel_df = pd.read_excel(uploaded_excel)
    optimal_df = pd.read_csv(uploaded_optimal, header=None, names=["블로그ID"])

    master_df, excel_df, selected_df = update_master(excel_df, optimal_df, st.session_state.master_df)

    st.session_state.master_df = master_df
    st.session_state.excel_df = excel_df

    st.success("필터링 완료 ✔")

# 화면표시
if st.session_state.excel_df is not None:
    left, right = st.columns(2)

    with left:
        st.subheader("📊 엑셀파일 중복 정리 결과")
        st.write(f"총 {len(st.session_state.excel_df)}개")
        st.dataframe(st.session_state.excel_df, use_container_width=True)

    with right:
        st.subheader("📌 최종 누적 리스트 (중복 제거 자동)")
        st.write(f"총 {len(st.session_state.master_df)}개")
        st.dataframe(st.session_state.master_df, use_container_width=True)

        csv = st.session_state.master_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📥 CSV 다운로드", csv, "누적리스트.csv", "text/csv")
