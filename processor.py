import pandas as pd
import re

CHAR_MAP = {
    '공': '0', '영': '0',
    '일': '1', '이': '2', '삼': '3', '사': '4',
    '오': '5', '육': '6', '륙': '6', '칠': '7', '팔': '8', '구': '9',
    'o': '0', 'O': '0',
    'l': '1', 'I': '1', 'i': '1',
    'Z': '2',
    'S': '5', 's': '5',
    'B': '8'
}

def normalize_phone(text):
    if not isinstance(text, str):
        return None

    clean = "".join(CHAR_MAP.get(ch, ch) for ch in text)
    clean = re.sub(r"[^0-9]", "", clean)

    match = re.search(r"(01[016789]\d{7,8})", clean)
    if match:
        number = match.group(1)
        if len(number) == 10:
            return f"{number[:3]}-{number[3:6]}-{number[6:]}"
        elif len(number) == 11:
            return f"{number[:3]}-{number[3:7]}-{number[7:]}"
    return None


def process_excel(file):
    df = pd.read_excel(file, dtype=str).fillna("")
    result = []

    for _, row in df.iterrows():
        user_id = row.iloc[0]
        phone_candidates = [row.iloc[1], row.iloc[3]]

        phone = None
        for p in phone_candidates:
            phone = normalize_phone(p)
            if phone:
                break

        result.append({"아이디": user_id, "전화번호": phone})

    result_df = pd.DataFrame(result)
    result_df = result_df.sort_values(by="전화번호", ascending=False).drop_duplicates(subset=["아이디"], keep="first")

    return result_df


def process_text(file):
    lines = file.read().decode("utf-8", "ignore").splitlines()
    return pd.DataFrame({"아이디": list(set(line.strip() for line in lines if line.strip()))})


def match_lists(excel_df, best_df):
    excel_ids = set(excel_df["아이디"].unique())
    matched_rows = []

    for _, row in best_df.iterrows():
        if row["아이디"] in excel_ids:
            phone = excel_df[excel_df["아이디"] == row["아이디"]].iloc[0]["전화번호"]
            matched_rows.append({"아이디": row["아이디"], "전화번호": phone, "메모": ""})

    return pd.DataFrame(matched_rows)
