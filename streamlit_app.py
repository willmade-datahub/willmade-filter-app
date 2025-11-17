import streamlit as st
import pandas as pd
import os
from processor import process_excel, match_lists

st.set_page_config(page_title="윌메이드 필터링 자동화", layout="wide")

st.title("📦 윌메이드 필터링 자동화 v2")

st.write("엑셀 + 최적리스트 업로드 후, 왼쪽/오른쪽 누적 리스트를 관리합니다.")

uploaded_excel = None
uploaded_optimal = None

col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 1) 파일 업로드")
    uploaded_excel = st.file_uploader("엑셀 파일 업로드", type=["xlsx"])
with col2:
    uploaded_optimal = st.file_uploader("최적 리스트 업로드", type=["txt", "csv"])

if st.button("🔍 필터링 실행") and uploaded_excel is not None and uploaded_optimal is not None:
    df_excel = pd.read_excel(uploaded_excel, engine="openpyxl")
    df_excel = process_excel(df_excel)

    optimal_ids = []
    for line in uploaded_optimal.read().decode("utf-8").splitlines():
        optimal_ids.append(line.strip())

    df_match = match_lists(df_excel, optimal_ids)

    # 메모 컬럼 추가
    df_match["메모"] = ""

    # 결과 저장
    df_excel.to_csv("left_storage.csv", index=False, encoding="utf-8-sig")
    df_match.to_csv("right_storage.csv", index=False, encoding="utf-8-sig")

    st.success("필터링 완료!")

# ===============================
# 누적 리스트 보여주기
# ===============================
st.subheader("📚 2) 누적 리스트 관리")

col_left, col_right = st.columns(2)

with col_left:
    st.write("📁 엑셀 전체 누적 리스트")
    if os.path.exists("left_storage.csv"):
        left_df = pd.read_csv("left_storage.csv")
        st.dataframe(left_df, use_container_width=True)

with col_right:
    st.write("🎯 최적 매칭 누적 리스트")
    if os.path.exists("right_storage.csv"):
        right_df = pd.read_csv("right_storage.csv")
        edited = st.data_editor(right_df, use_container_width=True)
        edited.to_csv("right_storage.csv", index=False, encoding="utf-8-sig")

# ===============================
# 초기화 버튼
# ===============================
if st.button("🧹 전체 데이터 초기화"):
    if os.path.exists("left_storage.csv"):
        os.remove("left_storage.csv")
    if os.path.exists("right_storage.csv"):
        os.remove("right_storage.csv")
    st.success("초기화 완료! 새롭게 진행하세요.")
