import pandas as pd
import re
from pathlib import Path

# =======================
# 경로 설정
# =======================
BASE_DIR = Path(__file__).parent
EXCEL_MASTER_PATH = BASE_DIR / "excel_master_list.csv"      # 왼쪽 누적
FILTERED_MASTER_PATH = BASE_DIR / "filtered_master_list.csv"  # 오른쪽 누적

# =======================
# 숫자 변환 매핑
# =======================
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

# =======================
# 전화번호 정규화
# =======================
def clean_phone(text: str) -> str:
    if not isinstance(text, str):
        return ""

    for k, v in KOR_NUM.items():
        text = text.replace(k, v)
    for k, v in ALPHA_NUM.items():
        text = text.replace(k, v)

    # 숫자만 남기기
    text = re.sub(r"[^0-9]", "", text)

    if len(text) == 10:
        return f"{text[:3]}-{text[3:6]}-{text[6:]}"
    elif len(text) == 11:
        return f"{text[:3]}-{text[3:7]}-{text[7:]}"
    return ""


# =======================
# 엑셀에서 아이디 / 전화번호 추출
#  - A열: 아이디
#  - B열 / D열: 전화번호 관련 텍스트
# =======================
def extract_from_excel(uploaded_excel) -> pd.DataFrame:
    df = pd.read_excel(uploaded_excel, dtype=str)

    # 엑셀 구조: 0=A열(아이디), 1=B열, 3=D열
    id_series = df.iloc[:, 0].fillna("").astype(str).str.strip()

    # B + D 합쳐서 하나의 텍스트로 보고 번호 뽑기
    col_b = df.iloc[:, 1] if df.shape[1] > 1 else ""
    col_d = df.iloc[:, 3] if df.shape[1] > 3 else ""

    raw_phone = col_b.fillna("").astype(str) + " " + col_d.fillna("").astype(str)
    phone_series = raw_phone.apply(clean_phone)

    result = pd.DataFrame(
        {
            "아이디": id_series,
            "전화번호": phone_series,
        }
    )

    # 전화번호 없는 행은 버리기
    result = result[result["전화번호"] != ""].copy()
    return result


# =======================
# 최적리스트(txt/csv)에서 아이디 집합 만들기
# =======================
def load_best_ids(uploaded_txt) -> set:
    content = uploaded_txt.read()
    try:
        text = content.decode("utf-8")
    except AttributeError:
        # 이미 str일 수도 있음
        text = str(content)
    except UnicodeDecodeError:
        text = content.decode("cp949", errors="ignore")

    ids = [line.strip() for line in text.splitlines() if line.strip()]
    return set(ids)


# =======================
# 누적 CSV 로딩/업데이트
# =======================
def load_cumulative(path: Path) -> pd.DataFrame:
    if path.exists():
        try:
            df = pd.read_csv(path, dtype=str)
        except Exception:
            df = pd.DataFrame(columns=["아이디", "전화번호", "처리"])
    else:
        df = pd.DataFrame(columns=["아이디", "전화번호", "처리"])

    if "처리" not in df.columns:
        df["처리"] = False
    else:
        df["처리"] = df["처리"].fillna(False).astype(bool)

    return df


def update_cumulative(path: Path, new_df: pd.DataFrame) -> pd.DataFrame:
    existing = load_cumulative(path)

    # 새 DF에도 처리 컬럼 추가
    if "처리" not in new_df.columns:
        new_df = new_df.copy()
        new_df["처리"] = False

    combined = pd.concat([existing, new_df], ignore_index=True)
    combined.drop_duplicates(subset=["아이디"], keep="first", inplace=True)

    combined.to_csv(path, index=False, encoding="utf-8-sig")
    return combined


# =======================
# 메인 처리 함수
#  - 반환값:
#      excel_master   : 엑셀 전체 누적
#      filtered_master: 최적리스트 매칭 누적
# =======================
def run_filtering(excel_file, best_file):
    # 1) 엑셀에서 전체 아이디/전화번호 추출
    excel_df = extract_from_excel(excel_file)

    # 2) 최적리스트 아이디 불러오기
    best_ids = load_best_ids(best_file)

    # 3) 최적리스트와 매칭된 부분만 추출 (오른쪽 리스트용)
    filtered_df = excel_df[excel_df["아이디"].isin(best_ids)].copy()

    # 4) 누적 저장 업데이트
    excel_master = update_cumulative(EXCEL_MASTER_PATH, excel_df)
    filtered_master = update_cumulative(FILTERED_MASTER_PATH, filtered_df)

    return excel_master, filtered_master, len(excel_df), len(filtered_df)


def load_all_cumulative():
    """앱 띄울 때 누적된 데이터 불러오는 헬퍼."""
    excel_master = load_cumulative(EXCEL_MASTER_PATH)
    filtered_master = load_cumulative(FILTERED_MASTER_PATH)
    return excel_master, filtered_master
