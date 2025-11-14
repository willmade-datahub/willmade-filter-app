import streamlit as st
import pandas as pd
from processor import update_master, load_master, STORAGE_PATH

st.set_page_config(page_title="윌메이드 필터링 자동화", page_icon="📦", layout="wide")

# 세션 상태 초기화
if "master_df" not in st.session_state:
    st.session_state.master_df = load_master()

st.title("📦 윌메이드 필터링 자동화")

uploaded_file = st.file_uploader("최적 리스트 업로드 (txt, csv)")

if st.button("필터링 실행"):
    if uploaded_file is not None:
        try:
            excel_df = pd.read_csv(uploaded_file, dtype=str)
            today_df, extracted_df = update_master(excel_df, st.session_state.master_df)
            st.session_state.master_df = today_df

            st.success("필터링 완료!")
            st.dataframe(extracted_df)

        except Exception as e:
            st.error(e)
    else:
        st.warning("파일을 업로드하세요.")

if st.button("초기화"):
    st.session_state.master_df = pd.DataFrame(columns=["아이디", "전화번호"])
    st.session_state.master_df.to_csv(STORAGE_PATH, index=False)
    st.success("초기화 완료")

st.download_button(
    label="최종 누적 리스트 다운로드",
    data=st.session_state.master_df.to_csv(index=False).encode("utf-8"),
    file_name="최종누적리스트.csv",
    mime="text/csv"
)

