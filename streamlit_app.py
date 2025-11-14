import streamlit as st
import pandas as pd

from processor import update_master, load_master

st.set_page_config(page_title="윌메이드 필터링 자동화", layout="wide")

st.title("📦 윌메이드 필터링 자동화")

# 세션에 마스터 DF 없으면 파일에서 로드
if "master_df" not in st.session_state:
    st.session_state.master_df = load_master()

st.subheader("📁 1) 파일 업로드")

uploaded_excel = st.file_uploader("엑셀 파일 업로드 (xlsx)", type=["xlsx"])
uploaded_optimal = st.file_uploader("최적 리스트 업로드 (txt, csv)", type=["txt", "csv"])

run = st.button("필터링 실행")

if run:
    if uploaded_excel is None or uploaded_optimal is None:
        st.error("두 개의 파일 모두 업로드 해주세요.")
    else:
        # 엑셀은 원본 그대로 읽되, 전부 문자열로
        raw_excel = pd.read_excel(uploaded_excel, dtype=str)

        # 최적 리스트 : 한 줄에 아이디 1개
        optimal_df = pd.read_csv(
            uploaded_optimal,
            header=None,
            names=["블로그ID"],
            dtype=str,
            encoding_errors="ignore",
        )

        # 마스터 갱신
        master_df, excel_clean_df, selected_df = update_master(
            raw_excel,
            optimal_df,
            st.session_state.master_df,
        )

        # 세션에도 반영
        st.session_state.master_df = master_df

        st.success("엑셀 필터링 완료 ✅")

        # ===== 화면 2분할 =====
        left, right = st.columns(2)

        with left:
            st.subheader(f"📊 엑셀파일 중복 정리 결과 (총 {len(excel_clean_df):,}개)")
            st.dataframe(excel_clean_df, use_container_width=True)

        with right:
            st.subheader(f"📌 최종 누적 리스트 (중복 제거 자동, 총 {len(master_df):,}개)")
            st.dataframe(master_df, use_container_width=True)

# 아래는 새로고침 후에도 항상 보이는 영역 (마스터가 비어있지 않을 때)
if len(st.session_state.master_df) > 0:
    st.markdown("---")
    st.subheader(f"📌 현재 저장된 최종 누적 리스트 (총 {len(st.session_state.master_df):,}개)")
    st.dataframe(st.session_state.master_df, use_container_width=True)
