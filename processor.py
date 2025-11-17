import pandas as pd
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
EXCEL_MASTER_PATH = BASE_DIR / "excel_master_list.csv"
FILTERED_MASTER_PATH = BASE_DIR / "filtered_master_list.csv"

# ===========================
# 한글·영문 숫자 → 숫자 변환
# ===========================
KOR_NUM = {
    "공": "0", "영": "0",
    "일": "1", "이": "2", "삼": "3", "사": "4",
    "오": "5", "육": "6", "륙": "6", "칠": "7", "팔": "8", "구": "9",
}

ALPHA_NUM = {
    "o": "0", "O": "0",
    "l": "1", "I": "1", "i": "1",
    "Z": "2",
    "S": "5", "s": "5",
    "B": "8",
}

def clean_phone(text: str) -> str:
    if not isinstance(text, str):
        return ""

    for k, v in KOR_NUM.items():
        text = text.replace(k, v)
    for k, v in ALPHA_NUM.items():
        text = text.replace(k, v)

    digits = re.sub(r"[^0-9]", "", text)

    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11:
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
    return ""

# ===========================
# 엑셀 파일 읽기 (A=아이디, B/D=전화번호)
# ===========================
def extract_from_excel(excel_file) -> pd.DataFrame:
    df = pd.read_excel(excel_file, dtype=str)

    id_series = df.iloc[:, 0].fillna("").astype(str).str.strip()
    col_b = df.iloc[:, 1].fillna("").astype(str)
    col_d = df.iloc[:, 3].fillna("").astype(str)

    phones = (col_b + " " + col_d).apply(clean_phone)

    return pd.DataFrame({
        "아이디": id_series,
        "전화번호": phones
    })

# ===========================
# 최적리스트 txt/csv
# ===========================
def load_best_ids(uploaded_txt) -> set:
    content = uploaded_txt.read()
    try:
        text = content.decode("utf-8")
    except:
        text = str(content)

    ids = [line.strip() for line in text.splitlines() if line.strip()]
    return set(ids)

# ===========================
# 누적 CSV 로드
# ===========================
def load_cumulative(path: Path, cols) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=cols)

    df = pd.read_csv(path, dtype=str)
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    return df

# ===========================
# 필터링 처리
# ===========================
def run_filtering(excel_file, best_file):
    excel_df = extract_from_excel(excel_file)
    best_ids = load_best_ids(best_file)

    filtered_df = excel_df[excel_df["아이디"].isin(best_ids)].copy()

    excel_master = update_master(EXCEL_MASTER_PATH, excel_df, cols=["아이디", "전화번호"])
    filtered_master = update_master(FILTERED_MASTER_PATH, filtered_df, cols=["아이디", "전화번호", "메모"])

    return excel_master, filtered_master

def update_master(path: Path, new_df: pd.DataFrame, cols):
    df = load_cumulative(path, cols)
    combined = pd.concat([df, new_df], ignore_index=True)
    combined.drop_duplicates(subset=["아이디"], inplace=True)
    combined.to_csv(path, index=False, encoding="utf-8-sig")
    return combined

# ===========================
# 초기화
# ===========================
def reset_all():
    if EXCEL_MASTER_PATH.exists():
        EXCEL_MASTER_PATH.unlink()
    if FILTERED_MASTER_PATH.exists():
        FILTERED_MASTER_PATH.unlink()
