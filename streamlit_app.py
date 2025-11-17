import streamlit as st
import pandas as pd

from processor import run_filtering, load_all_cumulative, EXCEL_MASTER_PATH, FILTERED_MASTER_PATH

st.set_page_config(
    page_title="윌메이드 필터링 자동화",
    layout="wide",
)

st.title("📦 윌메이드 필터링 자동화 v2")

st.markdown("엑셀 + 최적리스트 업로드 후, 왼쪽/오른쪽 누적 리스트로 관리합니다.")


# =======================
# 1) 파일 업로드 영역
# =======================
st.subheader("📁 1) 파일 업로드")

col_u1, col_u2 = st.columns(2)

with col_u1:
    excel_file = st.file_uploader("엑셀 파일 업로드 (xlsx)", type=["xlsx"])

with col_u2:
    best_file = st.file_uploader("최적 리스트 업로드 (txt, csv)", type=["txt", "csv"])


run_btn = st.button("🚀 필터링 실행")


# =======================
# 2) 필터링 실행
# =======================
if run_btn:
    if not excel_file or not best_file:
        st.warning("엑셀 파일과 최적 리스트 파일을 모두 업로드 해주세요.")
    else:
        with st.spinner("필터링 중입니다..."):
            excel_master, filtered_master, total_excel, total_filtered = run_filtering(
                excel_file, best_file
            )
        st.success(f"완료! 엑셀 {total_excel}건, 최적 매칭 {total_filtered}건 처리되었습니다.")

# =======================
# 3) 항상 누적 데이터 불러와서 보여주기
# =======================
excel_master, filtered_master = load_all_cumulative()

st.markdown("---")
st.subheader("📊 2) 누적 리스트 관리")

left_col, right_col = st.columns(2)

# 공통: 편집 가능한 테이블 함수
def editable_table(title, df: pd.DataFrame, csv_path, key_prefix: str):
    st.markdown(f"**{title}**  \n총 {len(df):,}건")
    if df.empty:
        st.info("데이터가 아직 없습니다.")
        return

    # 아이디 / 전화번호는 수정못하게, '처리'만 편집 가능하게
    # Streamlit 1.29+ 의 data_editor 사용
    edited_df = st.data_editor(
        df,
        column_config={
            "처리": st.column_config.CheckboxColumn("처리"),
        },
        disabled=["아이디", "전화번호"],
        num_rows="dynamic",
        key=f"{key_prefix}_editor",
        use_container_width=True,
    )

    # 변경 내용 저장
    if not edited_df.equals(df):
        edited_df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        st.toast("변경사항 저장 완료", icon="💾")


with left_col:
    editable_table(
        "왼쪽: 엑셀 전체 누적 리스트",
        excel_master,
        EXCEL_MASTER_PATH,
        key_prefix="excel_master",
    )

with right_col:
    editable_table(
        "오른쪽: 최적리스트 매칭 아이디+전화번호 누적 리스트",
        filtered_master,
        FILTERED_MASTER_PATH,
        key_prefix="filtered_master",
    )
