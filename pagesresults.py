import streamlit as st
import pandas as pd
from processor import load_master

PASSWORD = "sk23208689"

st.title("🔒 누적 리스트 보기")

pw = st.text_input("비밀번호 입력", type="password")

if pw != PASSWORD:
    st.warning("비밀번호가 일치해야 리스트가 표시됩니다.")
    st.stop()

st.success("비밀번호 확인 완료!")

df = load_master()
st.dataframe(df, height=500)

st.download_button(
    label="📥 누적 리스트 다운로드",
    data=df.to_csv(index=False).encode("utf-8-sig"),
    file_name="누적리스트.csv",
    mime="text/csv"
)
