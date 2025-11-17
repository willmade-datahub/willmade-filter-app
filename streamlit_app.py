import streamlit as st
import pandas as pd
from processor import run_filtering, load_cumulative, reset_all, EXCEL_MASTER_PATH, FILTERED_MASTER_PATH

st.set_page_config(page_title="윌메이드 필터링 자동화 v2", layout="wide")

st.title("📦 윌메이드 필터링 자동화 v2")

# ------------------ 업로드 -------------------
st.subheader("📁 1) 파일 업로드")
col1, col2 = st.columns(2)

with col1:
    excel_file = st.file_uploader("엑셀 파일 업로드 (xlsx)", type=["xlsx"])
with col2:
    best_file = st.file_uploader("최적 리스트 업로드 (txt/csv)", type=["txt", "csv"])

run_btn = st.button("🚀 필터링 실행", type="primary")
reset_btn = st.button("🗑 전체 초기화", type="secondary")

if reset_btn:
    reset_all()
    st.success("전체 누적 데이터 초기화 완료")
    st.experimental_rerun()

if run_btn:
    if not excel_file or not best_file:
        st.warning("두 파일 모두 업로드해주세요.")
    else:
        with st.spinner("처리 중..."):
            excel_master, filtered_master = run_filtering(excel_file, best_file)
        st.success("필터링 완료 🎉")

# ------------------ 누적 리스트 -------------------
st.markdown("---")
st.subheader("📊 2) 누적 리스트 관리")

excel_master = load_cumulative(EXCEL_MASTER_PATH, ["아이디", "전화번호"])
filtered_master = load_cumulative(FILTERED_MASTER_PATH, ["아이디", "전화번호", "메모"])

left, right = st.columns(2)

with left:
    st.markdown(f"### 📂 엑셀 전체 누적 리스트 (총 {len(excel_master)}건)")
    st.dataframe(excel_master, use_container_width=True)

with right:
    st.markdown(f"### 🎯 최적 매칭 누적 리스트 (총 {len(filtered_master)}건)")
    editable_filtered = st.data_editor(
        filtered_master,
        column_config={
            "메모": st.column_config.TextColumn("메모 입력"),
        },
        disabled=["아이디", "전화번호"],
        use_container_width=True,
        key="filtered_editor"
    )

    if not editable_filtered.equals(filtered_master):
        editable_filtered.to_csv(FILTERED_MASTER_PATH, index=False, encoding="utf-8-sig")
        st.toast("변경사항 저장 완료 💾")
