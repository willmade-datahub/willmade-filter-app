import streamlit as st
import pandas as pd
from processor import normalize_phone_numbers, load_master, save_master, merge_new_data

st.set_page_config(page_title="윌메이드 필터링 자동화", layout="wide")

st.markdown(
    "<h1 style='text-align:center; color:#000;'>윌메이드 필터링 자동화</h1>",
    unsafe_allow_html=True
)

# -------------------------
# 업로드 영역
# -------------------------
st.subheader("📁 1) 파일 업로드")

excel_file = st.file_uploader("엑셀 파일 업로드 (xlsx)", type=["xlsx"])
optimal_file = st.file_uploader("최적 리스트 업로드 (txt, csv)", type=["txt", "csv"])

if st.button("필터링 실행"):
    if excel_file is None:
        st.error("엑셀 파일을 먼저 업로드하세요.")
        st.stop()

    # 엑셀 읽기
    df = pd.read_excel(excel_file)

    # 컬럼 자동 인식
    id_col = df.columns[0]
    text_cols = df.columns[1:]

    # 전화번호 추출
    df["전화번호"] = df[text_cols].astype(str).apply(
        lambda row: normalize_phone_numbers(" ".join(row.values)), axis=1
    )

    preview = df[[id_col, "전화번호"]]
    st.success("엑셀 필터링 완료")

    st.subheader("📄 2) 오늘 업로드된 엑셀 결과")
    st.dataframe(preview, height=300)

    # 누적 리스트 처리
    master = load_master()
    updated_master = merge_new_data(master, preview, id_col)
    save_master(updated_master)

    # 최적리스트 처리
    if optimal_file is not None:
        try:
            opt_ids = pd.read_csv(optimal_file, header=None)[0].astype(str).tolist()
        except:
            opt_ids = pd.read_csv(optimal_file, sep="\t", header=None)[0].astype(str).tolist()

        matched = updated_master[updated_master[id_col].isin(opt_ids)]
        st.subheader("🎯 3) 최적 리스트에서 선별된 결과")
        st.dataframe(matched, height=300)

st.info("좌측 메뉴 '누적 리스트 보기'에서 전체 누적 데이터를 확인할 수 있습니다.")
