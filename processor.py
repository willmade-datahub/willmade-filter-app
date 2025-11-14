import pandas as pd
import re
import os

STORAGE = "storage/master_list.csv"

# 전화번호 치환 규칙
replace_map = {
    "공": "0", "영": "0", "o": "0", "O": "0",
    "일": "1", "I": "1", "l": "1",
    "이": "2",
    "삼": "3",
    "사": "4",
    "오": "5",
    "육": "6",
    "칠": "7",
    "팔": "8",
    "구": "9",
}

def normalize_phone_numbers(text):
    if pd.isna(text):
        return ""

    s = str(text)
    for k,v in replace_map.items():
        s = s.replace(k, v)

    digits = re.findall(r"(010[-\s]?\d{4}[-\s]?\d{4})|(\d{11})", s)
    numbers = []
    for tup in digits:
        raw = "".join(tup)
        raw = re.sub(r"\D", "", raw)
        if len(raw) == 11 and raw.startswith("010"):
            numbers.append(f"{raw[0:3]}-{raw[3:7]}-{raw[7:11]}")

    return " / ".join(sorted(list(set(numbers))))

def load_master():
    if not os.path.exists(STORAGE):
        return pd.DataFrame(columns=["아이디", "전화번호"])
    return pd.read_csv(STORAGE)

def save_master(df):
    df.to_csv(STORAGE, index=False)

def merge_new_data(master, new, id_col):
    new = new.rename(columns={id_col: "아이디"})
    if "전화번호" not in new.columns:
        new["전화번호"] = ""

    new = new.groupby("아이디")["전화번호"].apply(lambda x: " / ".join(x.dropna())).reset_index()

    for _, row in new.iterrows():
        uid = row["아이디"]
        uphone = row["전화번호"]

        if uid in master["아이디"].values:
            old_phone = master.loc[master["아이디"]==uid, "전화번호"].iloc[0]

            if old_phone.strip() == "":
                master.loc[master["아이디"]==uid, "전화번호"] = uphone
                continue

            merged = sorted(list(set(old_phone.split(" / ") + uphone.split(" / "))))
            master.loc[master["아이디"]==uid, "전화번호"] = " / ".join(merged)
        else:
            master.loc[len(master)] = [uid, uphone]

    master.drop_duplicates(subset=["아이디"], keep="first", inplace=True)
    return master
