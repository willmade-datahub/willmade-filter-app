# streamlit_app.py
import os

import pandas as pd
import streamlit as st

from processor import update_master, load_master, STORAGE_PATH

st.set_page_config(page_title="윌메이드 필터링 자동화", layout="wide")

st.title("📦 윌메이드 필터링 자동화")

# ------------------------------
# 0) 세션에 마스터 DF 로드
# ------------------------------
if "master_df" not in st.session_state:
    st.session_state.master_df = load_master()

# ------------------------------
# 1) 파일 업로드 섹션
# ------------------------------
st.subheader("📁 1) 파일 업로드")

uploaded_excel = st.file_uploader("엑셀 파일 업로드 (xlsx)", type=["xlsx"])

btn_col1, btn_col2 = st.columns([1, 1])
with btn_col1:
    run_clicked = st.button("필터링 실행")
with btn_col2:
    reset_clicked = st.button("누적 리스트 초기화", type="secondary")

# ------------------------------
# 2) 초기화 버튼 동작
# ------------------------------
if reset_clicked:
    if os.path.exists(STORAGE_PATH):
        os.remove(STORAGE_PATH)
    st.session_state.master_df = load_master()
    st.success("✅ 누적 리스트를 초기화했습니다.")

today_df = None

# ------------------------------
# 3) 필터링 실행 버튼 동작
# ------------------------------
if run_clicked:
    if uploaded_excel is None:
        st.error("엑셀 파일을 먼저 업로드 해주세요.")
    else:
        # 원본 엑셀은 컬럼 이름 신경 안 쓰고, A/B/D 열 기준으로 처리
        excel_df = pd.read_excel(uploaded_excel, dtype=str)

        master_df = st.session_state.master_df
        new_master, today_df = update_master(excel_df, master_df)

        st.session_state.master_df = new_master
        st.success("✔ 필터링 완료")

# ------------------------------
# 4) 결과 화면 2분할 표시
# ------------------------------
master_df = st.session_state.master_df

left, right = st.columns(2)

with left:
    st.subheader("📊 엑셀파일 중복 정리 결과")
    if today_df is not None:
        st.caption(f"총 {len(today_df):,}개")
        st.dataframe(today_df, use_container_width=True, height=600)
    else:
        st.info("아직 오늘 업로드된 결과가 없습니다. 엑셀을 올리고 **필터링 실행**을 눌러주세요.")

with right:
    st.subheader("📌 최종 누적 리스트 (중복 제거 자동)")
    st.caption(f"총 {len(master_df):,}개")
    st.dataframe(master_df, use_container_width=True, height=600)
