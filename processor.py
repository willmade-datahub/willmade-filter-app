import pandas as pd
import re

# 전화번호 추출 함수
def extract_phone(text):
    if pd.isna(text):
        return None
    pattern = r'(01[016789])[-\s\.\)]?(\d{3,4})[-\s\.\(]?(\d{4})'
    match = re.search(pattern, str(text))
    if match:
        return f"{match.group(1)}{match.group(2)}{match.group(3)}"
    return None

# 메인 처리 함수
def update_master(excel_df, optimal_df):
    # A열(Blogger ID)
    excel_df['블로그ID'] = excel_df.iloc[:, 0]

    # B열 + D열에서 전화번호 추출
    excel_df['전화번호'] = excel_df.iloc[:, 1].astype(str) + " " + excel_df.iloc[:, 3].astype(str)
    excel_df['전화번호'] = excel_df['전화번호'].apply(extract_phone)

    # 전화번호 없는 행 제거
    excel_df = excel_df.dropna(subset=['전화번호'])

    # 중복 제거 (전화번호 기준)
    excel_df = excel_df.drop_duplicates(subset=['전화번호'], keep='first')

    # 필요한 컬럼만 반환
    result_df = excel_df[['블로그ID', '전화번호']]

    return result_df, excel_df, optimal_df
