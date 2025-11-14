import pandas as pd
from pathlib import Path

# 누적 리스트 저장 파일
STORAGE_PATH = Path("storagemaster_list.csv")


def load_master() -> pd.DataFrame:
    if STORAGE_PATH.exists():
        try:
            df = pd.read_csv(STORAGE_PATH, dtype=str)
            if df.empty:
                return pd.DataFrame(columns=["블로그ID", "전화번호"])
            return df
        except:
            return pd.DataFrame(columns=["블로그ID", "전화번호"])
    else:
        return pd.DataFrame(columns=["블로그ID", "전화번호"])

def _extract_phone(text: str) -> str:
    """
    본문에서 전화번호 한 개 추출 (간단 버전)
    010-XXXX-XXXX / 010XXXXXXXX 형식 등 숫자 위주로 잡기
    """
    if pd.isna(text):
        return ""
    s = str(text)

    # 01로 시작하는 번호 패턴 대충 뽑기
    import re
    m = re.search(r"(01[016789][0-9\-]{7,11})", s)
    if not m:
        return ""

    raw = m.group(1)
    # 숫자만 남기기
    digits = re.sub(r"[^0-9]", "", raw)

    # 010-0000-0000 형식으로 맞추기 (길이 11인 경우만)
    if len(digits) == 11:
        return f"{digits[0:3]}-{digits[3:7]}-{digits[7:]}"
    return digits


def update_master(excel_df: pd.DataFrame,
                  optimal_df: pd.DataFrame,
                  master_df: pd.DataFrame | None = None):
    """
    excel_df : 원본 엑셀 (A열=아이디, B열=제목, D열=본문(검색어+연락처))
    optimal_df : 최적 리스트 (한 줄에 아이디 하나)
    master_df : 기존 누적 리스트 (없으면 파일에서 로드)

    반환:
      master_df(갱신된 누적), excel_clean_df(엑셀 정리본), selected_df(이번에 뽑힌 최적)
    """

    # 1) 마스터 로드
    if master_df is None:
        master_df = load_master()

    # 2) 엑셀에서 필요한 열만 사용 (A,B,D 고정)
    #    0: 아이디, 1: 제목, 3: 본문(연락처 포함)
    id_col = excel_df.columns[0]
    title_col = excel_df.columns[1]
    body_col = excel_df.columns[3]

    work_df = excel_df[[id_col, title_col, body_col]].copy()
    work_df.columns = ["블로그ID", "제목", "본문"]

    # 문자열로 고정 (strip 같은 거 절대 안 함)
    work_df["블로그ID"] = work_df["블로그ID"].astype(str)

    # 3) 본문에서 전화번호 추출
    work_df["전화번호"] = work_df["본문"].apply(_extract_phone)

    # 엑셀 정리 결과(아이디 기준 중복 제거 - 완전히 같은 아이디만)
    excel_clean_df = work_df[["블로그ID", "제목", "전화번호"]].drop_duplicates(
        subset=["블로그ID"], keep="first"
    )

    # 4) 최적 리스트 아이디와 교집합만 추출
    optimal_ids = optimal_df["블로그ID"].astype(str).tolist()
    selected_df = excel_clean_df[excel_clean_df["블로그ID"].isin(optimal_ids)].copy()

    # 5) 누적 리스트 갱신 (아이디 완전 동일할 때만 중복 제거)
    combined = pd.concat([master_df, selected_df], ignore_index=True)
    combined = combined.drop_duplicates(subset=["블로그ID"], keep="first")

    # 6) CSV로 저장 (새로고침해도 파일은 남음)
    combined.to_csv(STORAGE_PATH, index=False, encoding="utf-8-sig")

    return combined, excel_clean_df, selected_df

