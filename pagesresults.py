import streamlit as st
import pandas as pd

st.set_page_config(page_title="누적 리스트 보기")

st.title("📦 누적 리스트 전체 보기")

try:
    df = pd.read_csv("storagemaster_list.csv")
    st.dataframe(df, use_container_width=True)
except:
    st.info("아직 저장된 누적 데이터가 없습니다.")
