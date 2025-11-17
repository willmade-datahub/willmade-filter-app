import streamlit as st
import pandas as pd
from processor import load_all_cumulative

st.set_page_config(page_title="누적 리스트 전체 보기", layout="wide")

st.title("📑 🧾 누적 리스트 전체 보기")

excel_master, filtered_master = load_all_cumulative()

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"엑셀 전체 누적 ({len(excel_master):,}건)")
    st.dataframe(excel_master, use_container_width=True)

with col2:
    st.subheader(f"최적 매칭 누적 ({len(filtered_master):,}건)")
    st.dataframe(filtered_master, use_container_width=True)
