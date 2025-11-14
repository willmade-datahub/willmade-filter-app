import pandas as pd
import re

def extract_phone(text):
    phones = re.findall(r'01[016789]-?\d{3,4}-?\d{4}', str(text))
    return phones[0] if phones else None

def update_master(excel_df, optimal_df, master_df):
    # 엑셀 데이터에서 필요한 A,B,D 컬럼만 사용
    excel_df = excel_df.iloc[:, [0,1,3]]
    excel_df.columns = ["블로그ID", "제목", "본문"]

    # 전화번호 추출
    excel_df["전화번호"] = excel_df["본문"].apply(extract_phone)

    # 전화번호 없는 행 제거
    excel_df = excel_df.dropna(subset=["전화번호"])

    # 중복 제거 (ID 기준)
    excel_df = excel_df.drop_duplicates(subset=["블로그ID"])

    # 최적리스트 ID 매칭
    selected_df = excel_df[excel_df["블로그ID"].isin(optimal_df["블로그ID"])][["블로그ID", "전화번호"]]

    # 누적 리스트 저장 (session master_df + selected_df)
    if master_df is None:
        master_df = selected_df
    else:
        master_df = pd.concat([master_df, selected_df])
        master_df = master_df.drop_duplicates(subset=["블로그ID"]).reset_index(drop=True)

    return master_df, excel_df, selected_df
