import pandas as pd
import re
import os

STORAGE_PATH = "master_list.csv"

def clean_phone(text):
    if pd.isna(text):
        return ""
    text = str(text)
    text = re.sub(r"[^0-9]", "", text)
    if text.startswith("82"):
        text = "0" + text[2:]
    if len(text) == 10:
        text = text[:3] + text[3:6] + text[6:]
    if len(text) != 11:
        return ""
    return text

def load_master():
    if os.path.exists(STORAGE_PATH):
        return pd.read_csv(STORAGE_PATH)
    else:
        return pd.DataFrame(columns=["블로그ID", "전화번호"])

def update_master(excel_df, optimal_df):
    excel_df["전화번호"] = excel_df.apply(
        lambda row: clean_phone(str(row.iloc[1]) + str(row.iloc[3])), axis=1
    )
    excel_df = excel_df.rename(columns={excel_df.columns[0]: "블로그ID"})
    excel_df = excel_df[["블로그ID", "전화번호"]]

    # ID 기준 완전일치 중복 제거
    excel_df = excel_df.drop_duplicates(subset=["블로그ID"], keep="first")

    # 최적리스트에서 ID만 남기기
    selected_df = excel_df[excel_df["블로그ID"].isin(optimal_df["블로그ID"])]

    # 기존 저장파일 불러오기
    master_df = load_master()

    # 합치기 + 중복 제거
    master_df = pd.concat([master_df, selected_df], ignore_index=True).drop_duplicates(
        subset=["블로그ID"], keep="first"
    )

    master_df.to_csv(STORAGE_PATH, index=False)
    return master_df, excel_df, selected_df
