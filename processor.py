import re
import pandas as pd

# ===============================
# 전화번호 문자 → 숫자 변환 매핑
# ===============================
NUM_MAP = {
    '공': '0', '영': '0',
    '일': '1', '이': '2', '삼': '3', '사': '4',
    '오': '5', '육': '6', '륙': '6', '칠': '7', '팔': '8', '구': '9',
    'o': '0', 'O': '0',
    'l': '1', 'I': '1', 'i': '1',
    'Z': '2',
    'S': '5', 's': '5',
    'B': '8'
}

def normalize_characters(text):
    result = []
    for ch in text:
        if ch in NUM_MAP:
            result.append(NUM_MAP[ch])
        else:
            result.append(ch)
    return "".join(result)

# ===============================
# 전화번호 추출 함수
# ===============================
def extract_phone(text):
    if pd.isna(text):
        return None

    text = normalize_characters(str(text))

    # 숫자 아닌 모든 문자 제거
    digits = re.sub(r'[^0-9]', '', text)

    # 10자리 또는 11자리만 인정
    if len(digits) == 10:
        return f"{digits[0:3]}-{digits[3:6]}-{digits[6:10]}"
    if len(digits) == 11:
        return f"{digits[0:3]}-{digits[3:7]}-{digits[7:11]}"

    return None

# ===============================
# 엑셀 데이터 처리 함수
# ===============================
def process_excel(df):
    df_filtered = pd.DataFrame()
    df_filtered["아이디"] = df.iloc[:, 0]
    phones = []

    for row in df.iloc[:, 1:].astype(str).values:
        combined = " ".join(row)
        phones.append(extract_phone(combined))

    df_filtered["전화번호"] = phones
    return df_filtered

# ===============================
# 선별리스트 비교
# ===============================
def match_lists(df_excel, optimal_ids):
    return df_excel[df_excel["아이디"].isin(optimal_ids)].reset_index(drop=True)
