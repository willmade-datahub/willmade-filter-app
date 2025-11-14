import pandas as pd
import re
import os

STORAGE_PATH = "master.csv"

normalize_dict = {
    "o":"0","O":"0","공":"0","영":"0",
    "l":"1","I":"1","일":"1","하나":"1",
    "이":"2","둘":"2",
    "삼":"3","세":"3",
    "사":"4","네":"4",
    "오":"5",
    "육":"6","륙":"6",
    "칠":"7",
    "팔":"8",
    "구":"9",
}

def clean_phone(raw):
    if pd.isna(raw):
        return ""

    text = str(raw)
    text = text.replace("ㅣ", "1")

    for k, v in normalize_dict.items():
        text = text.replace(k, v)

    numbers = re.sub(r'[^0-9]', "", text)

    match = re.search(r"01[016789][0-9]{7,8}", numbers)
    return match.group(0) if match else ""

def load_master():
    if os.path.exists(STORAGE_PATH):
        return pd.read_csv(STORAGE_PATH)
    return pd.DataFrame(columns=["아이디","전화번호"])

def update_master(excel_df, optimal_df, master_df):
    # --- 아이디 컬럼 통일 ---
    excel_df.rename(columns={excel_df.columns[0]: "아이디"}, inplace=True)

    # --- 전화번호 추출 (엑셀 B,D 열에서 추출) ---
    excel_df["전화번호_B"] = excel_df.iloc[:,1].apply(clean_phone)
    excel_df["전화번호_D"] = excel_df.iloc[:,3].apply(clean_phone)
    excel_df["전화번호"] = excel_df["전화번호_B"].combine_first(excel_df["전화번호_D"])

    # --- 필요한 컬럼만 사용 ---
    today_df = excel_df[["아이디", "전화번호"]]

    # --- 엑셀 중복 제거 ---
    today_df.drop_duplicates(subset=["아이디"], keep="first", inplace=True)

    # --- 최적리스트와 비교해서 일치하는 ID만 추출 ---
    merged_df = pd.merge(optimal_df, today_df, on="아이디", how="inner")

    # --- 기존 master와 합치고 중복 제거 ---
    combined_df = pd.concat([master_df, merged_df])
    combined_df.drop_duplicates(subset=["아이디"], keep="first", inplace=True)

    # --- 저장 ---
    combined_df.to_csv(STORAGE_PATH, index=False)

    return combined_df, today_df, merged_df
