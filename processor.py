import pandas as pd
import os

STORAGE_PATH = "master_list.csv"

def load_master():
    try:
        if not os.path.exists(STORAGE_PATH):
            return pd.DataFrame(columns=["아이디", "전화번호"])

        df = pd.read_csv(STORAGE_PATH, dtype=str)

        if df.empty:
            return pd.DataFrame(columns=["아이디", "전화번호"])

        return df
    except:
        return pd.DataFrame(columns=["아이디", "전화번호"])

def clean_phone(x):
    if pd.isna(x):
        return None
    # 숫자만 추출
    digits = re.sub(r"[^0-9]", "", str(x))
    if len(digits) == 11 and digits.startswith("010"):
        return digits
    return None

def update_master(excel_df, master_df):
    # 전화번호 정제
    excel_df["전화번호_B"] = excel_df.iloc[:, 1].apply(clean_phone)
    excel_df["전화번호_D"] = excel_df.iloc[:, 3].apply(clean_phone)

    excel_df["전화번호"] = excel_df["전화번호_B"].combine_first(excel_df["전화번호_D"])
    today_df = excel_df[["아이디", "전화번호"]]

    today_df = today_df.dropna(subset=["전화번호"])
    today_df = today_df[~today_df["아이디"].isin(master_df["아이디"])]

    master_df = pd.concat([master_df, today_df], ignore_index=True)
    master_df.to_csv(STORAGE_PATH, index=False)

    return master_df, today_df

