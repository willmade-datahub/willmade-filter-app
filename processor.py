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
    excel_df["전화번호"] = excel_df.iloc[:,1].apply(clean_phone).combine_first(
        excel_df.iloc[:,3].apply(clean_phone)
    )

    today_df = excel_df[["아이디", "전화번호"]]
    today_df.drop_duplicates(subset=["아이디"], inplace=True)

    merged_df = pd.merge(optimal_df, today_df, on="아이디", how="inner")

    combined_df = pd.concat([master_df, merged_df])
    combined_df.drop_duplicates(subset=["아이디"], keep="first", inplace=True)

    combined_df.to_csv(STORAGE_PATH, index=False)

    return combined_df, today_df, merged_df
