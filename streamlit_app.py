
import streamlit as st
import pandas as pd

st.title("🔍 윌메이드 필터링 자동화 웹앱")

st.write("엑셀 업로드 → 아이디/전화번호 추출 → 최적 리스트 필터링 → 결과 다운로드")

uploaded_file = st.file_uploader("📂 엑셀 파일 업로드 (xlsx)", type=["xlsx"])
best_list_file = st.file_uploader("📂 최적 리스트 (txt 또는 csv)", type=["txt", "csv"])

def extract_phone(text):
    import re
    if pd.isna(text):
        return None
    patterns = [
        r'01[0-9]-\d{3,4}-\d{4}',
        r'01[0-9]\d{7,8}'
    ]
    for p in patterns:
        m = re.search(p, str(text))
        if m:
            return m.group()
    return None

if st.button("🚀 필터링 실행"):
    if uploaded_file is None:
        st.error("엑셀 파일을 업로드해주세요.")
    else:
        df = pd.read_excel(uploaded_file)

        if "아이디" not in df.columns:
            st.error("엑셀에 '아이디' 컬럼이 없습니다.")
        else:
            if "내용" in df.columns:
                df["전화번호"] = df["내용"].apply(extract_phone)
            else:
                df["전화번호"] = None

            df = df.drop_duplicates(subset=["아이디"], keep="first")

            if best_list_file:
                best_list = pd.read_csv(best_list_file, header=None).iloc[:, 0].astype(str)
                df = df[df["아이디"].astype(str).isin(best_list.astype(str))]

            output_path = "필터링완료.xlsx"
            df.to_excel(output_path, index=False)

            with open(output_path, "rb") as f:
                st.download_button(
                    label="📥 필터링된 엑셀 다운로드",
                    data=f,
                    file_name="필터링완료.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            st.success("🎉 완료되었습니다!")
