import pandas as pd
import re

# ===========================
# 한글 / 영문 → 숫자 변환 매핑
# ===========================
KOR_ENG_MAP = str.maketrans({
    '공': '0', '영': '0',
    '일': '1', '이': '2', '삼': '3', '사': '4',
    '오': '5', '육': '6', '륙': '6', '칠': '7', '팔': '8', '구': '9',

    'o': '0', 'O': '0',
    'l': '1', 'I': '1', 'i': '1',
    'Z': '2',
    'S': '5', 's': '5',
    'B': '8'
})


# ===========================
# 전화번호 정제 + 추출 함수
# ===========================
def extract_phone(text):
    if not text:
        return None

    # 문자 → 숫자 변환
    converted = text.translate(KOR_ENG_MAP)

    # 줄바꿈 / 탭 / 특수문자 정리
    converted = converted.replace("\n", " ").replace("\r", " ").replace("\t", " ")

    # 숫자, 공백 제외하고 제거 (011-565-0701 / 010 5652 0701 등)
    converted = re.sub(r'[^0-9 ]', ' ', converted)

    # 다중 공백 하나로
    converted = re.sub(r'\s+', ' ', converted)

    # 패턴 검출
    pattern = r'(01[016789])\s*([0-9]{3,4})\s*([0-9]{4})'
    match = re.search(pattern, converted)

    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
    return None


# ===========================
# 엑셀 파일 처리
# ===========================
def process_excel(file):
    df = pd.read_excel(file)

    result = []
    for idx, row in df.iterrows():
        user_id = str(row.iloc[0]).strip()  # A열 (아이디)
        # B열, D열에서 전화번호 추출
        phone1 = extract_phone(str(row.iloc[1])) if len(row) > 1 else None
        phone2 = extract_phone(str(row.iloc[3])) if len(row) > 3 else None

        phone = phone1 if phone1 else phone2
        result.append({"아이디": user_id, "전화번호": phone})

    return pd.DataFrame(result)


# ===========================
# 텍스트 파일(최적리스트) 처리
# ===========================
def process_text(file):
    lines = file.read().decode('utf-8', errors='ignore').splitlines()
    return pd.DataFrame({"아이디": [line.strip() for line in lines if line.strip()]})
