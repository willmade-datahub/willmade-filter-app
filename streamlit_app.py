import streamlit as st
import pandas as pd
import os
from processor import update_master, load_master, STORAGE_PATH

st.set_page_config(page_title="윌메이드 필터링 자동화", layout="wide")
st.title("📦 윌메이드 필터링 자동화")

# --- 저장된 master.csv 불러오기 ---
if "master_df" not in st.session_state:
    st.session_state.master_df = load_master()

st.subheader("📁 1) 파일 업로드")

uploaded_excel = st.file_uploader("엑셀 파일 업로드 (xlsx)", type=["xlsx"])
uploaded_optimal = st.file_uploader("최적 리스트 업로드 (txt, csv)", type=["txt", "csv"])

if st.button("필터링 실행"):
    if uploaded_excel is None or uploaded_optimal is None:
        st.error("두 개의 파일 모두 업로드 해주세요.")
    else:
        excel_df = pd.read_excel(uploaded_excel)
        optimal_df = pd.read_csv(uploaded_optimal, header=None, names=["아이디"])

        st.session_state.master_df, today_df, extracted_df = update_master(excel_df, optimal_df, st.session_state.master_df)

        st.success("필터링 완료 🎉")

        left, right = st.columns(2)

        with left:
            st.subheader(f"📊 엑셀파일 중복 정리 결과 (총 {len(today_df)}개)")
            st.dataframe(today_df, use_container_width=True)

        with right:
            st.subheader(f"📌 최종 누적 리스트 (중복 제거 자동, 총 {len(st.session_state.master_df)}개)")
            st.dataframe(st.session_state.master_df, use_container_width=True)

st.divider()

if st.button("🧹 최종 누적 리스트 초기화"):
    st.session_state.master_df = pd.DataFrame(columns=["아이디", "전화번호"])
    st.session_state.master_df.to_csv(STORAGE_PATH, index=False)
    st.success("초기화 완료! 리스트가 완전히 비워졌습니다.")
