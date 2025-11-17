import pandas as pd
import re

# ==========================
# 전화번호 문자 → 숫자 변환 매핑
# ==========================
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

    # 010xxxxxxxx 형식 추출
    match = re.search(r"(01[016789]\d{7,8})", clean)
    if match:
        number = match.group(1)
        if len(number) == 10:
            return f"{number[:3]}-{number[3:6]}-{number[6:]}"
        elif len(number) == 11:
            return f"{number[:3]}-{number[3:7]}-{number[7:]}"
    return None


# ==========================
# 엑셀 처리 함수
# ==========================
def process_excel(file):
    df = pd.read_excel(file, dtype=str).fillna("")
    result = []

    for _, row in df.iterrows():
        user_id = row.iloc[0]
        phone_candidates = [row.iloc[1], row.iloc[3]]  # B열, D열

        phone = None
        for p in phone_candidates:
            phone = normalize_phone(p)
            if phone:
                break

        result.append({"아이디": user_id, "전화번호": phone})

    return pd.DataFrame(result)


# ==========================
# 최적 리스트 TXT 처리
# ==========================
def process_text(file):
    lines = file.read().decode("utf-8", "ignore").splitlines()
    return pd.DataFrame({"아이디": list(set(line.strip() for line in lines if line.strip()))})


# ==========================
# 매칭
# ==========================
def match_lists(excel_df, best_df):
    excel_ids = set(excel_df["아이디"].unique())
    matched_rows = []

    for _, row in best_df.iterrows():
        if row["아이디"] in excel_ids:
            excel_match = excel_df[excel_df["아이디"] == row["아이디"]]
            phone = excel_match.iloc[0]["전화번호"]
            matched_rows.append({"아이디": row["아이디"], "전화번호": phone, "메모": None})

    return pd.DataFrame(matched_rows)
