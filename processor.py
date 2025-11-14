# processor.py
import os
import re
import pandas as pd

# 누적 리스트 저장 파일 경로
STORAGE_PATH = "storagemaster_list.csv"


# ------------------------------
# 1) 전화번호 정리 함수
# ------------------------------
def clean_phone(text: str) -> str:
    """문자열에서 휴대폰 번호 한 개를 뽑아서 010-1234-5678 형식으로 리턴.
    없으면 빈 문자열("") 리턴.
    """

    if not isinstance(text, str):
        text = str(text)

    # 한글/비슷한 글자를 숫자로 치환
    mapping = {
        "O": "0",
        "o": "0",
        "ㅇ": "0",
        "영": "0",
        "공": "0",
        "l": "1",
        "I": "1",
        "ㅣ": "1",
        "이": "2",
        "삼": "3",
        "사": "4",
        "오": "5",
        "육": "6",
        "윽": "6",
        "칠": "7",
        "ㅊ": "7",
        "팔": "8",
        "발": "8",
        "구": "9",
    }

    normalized = []
    for ch in text:
        normalized.append(mapping.get(ch, ch))
    text = "".join(normalized)

    # 숫자만 남기기
    digits = re.sub(r"[^0-9]", "", text)

    # 너무 짧으면 버림
    if len(digits) < 9:
        return ""

    # 국가코드 82 처리
    if digits.startswith("8210"):
        digits = "0" + digits[2:]  # 8210 → 010
    elif digits.startswith("82") and not digits.startswith("8210"):
        digits = "0" + digits[2:]

    # 10xxxxx 이런 식이면 앞에 0 붙이기
    if digits.startswith("10") and len(digits) == 11:
        digits = "0" + digits

    # 010으로 시작하면 11자리까지만 사용
    if digits.startswith("010") and len(digits) >= 11:
        digits = digits[:11]

    # 자리수에 따라 하이픈 넣기
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11:
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
    else:
        return ""


# ------------------------------
# 2) 누적 리스트 로드 / 저장
# ------------------------------
def load_master() -> pd.DataFrame:
    """저장된 누적 리스트를 불러오기. 없으면 빈 DF."""
    if os.path.exists(STORAGE_PATH):
        try:
            df = pd.read_csv(STORAGE_PATH, dtype=str)
            if df.empty:
                return pd.DataFrame(columns=["아이디", "전화번호"])
            return df
        except:
            return pd.DataFrame(columns=["아이디", "전화번호"])
    else:
        return pd.DataFrame(columns=["아이디", "전화번호"])

def save_master(df: pd.DataFrame) -> None:
    """누적 리스트를 CSV로 저장."""
    df.to_csv(STORAGE_PATH, index=False, encoding="utf-8-sig")


# ------------------------------
# 3) 엑셀 + 기존 마스터 합치기
# ------------------------------
def update_master(excel_df: pd.DataFrame, master_df: pd.DataFrame):
    """엑셀에서 아이디/전화번호 뽑아서 기존 마스터와 합치고 저장."""

    # A열 = 아이디 (0번째 컬럼)
    ids = excel_df.iloc[:, 0].astype(str)

    # B열 / D열 텍스트 (없는 경우는 빈 문자열)
    col_b = (
        excel_df.iloc[:, 1].astype(str)
        if excel_df.shape[1] > 1
        else pd.Series([""] * len(excel_df))
    )
    col_d = (
        excel_df.iloc[:, 3].astype(str)
        if excel_df.shape[1] > 3
        else pd.Series([""] * len(excel_df))
    )

    phones = []
    for b, d in zip(col_b, col_d):
        # D열(본문)을 우선, 없으면 B열(제목)에서 추출
        p = clean_phone(d)
        if not p:
            p = clean_phone(b)
        phones.append(p)

    # 오늘 엑셀에서 뽑은 결과
    today_df = pd.DataFrame({"아이디": ids, "전화번호": phones})

    # 전화번호 없는 행은 제거
    today_df = today_df[today_df["전화번호"] != ""]

    # 오늘 데이터 안에서 아이디 중복 제거
    today_df = today_df.drop_duplicates(subset="아이디", keep="first")

    # 기존 마스터와 합치기
    if master_df is None or master_df.empty:
        new_master = today_df.copy()
    else:
        combined = pd.concat([master_df, today_df], ignore_index=True)
        # 아이디가 **완전히 같은 것만** 중복으로 보고 제거
        new_master = combined.drop_duplicates(subset="아이디", keep="first")

    # 저장
    save_master(new_master)

    # new_master = 전체 누적, today_df = 이번에 올린 엑셀에서 뽑힌 것만
    return new_master, today_df

