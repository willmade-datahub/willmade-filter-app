def clean_phone(text):
    if pd.isna(text):
        return ""
    text = str(text)
    # 한글 숫자 치환
    kor_num = {"영":"0","공":"0","하나":"1","둘":"2","셋":"3","삼":"3","넷":"4","다섯":"5","오":"5","육":"6","칠":"7","팔":"8","구":"9"}
    for k,v in kor_num.items():
        text = text.replace(k, v)

    # 숫자만 추출
    numbers = "".join([c for c in text if c.isdigit()])
    if len(numbers) == 10:  # 010 제외된 경우
        numbers = "0" + numbers
    if len(numbers) == 11:
        return numbers
    return ""

def update_master(excel_df, optimal_df, master_df):
    # A열 = ID
    excel_df["아이디"] = excel_df.iloc[:, 0].astype(str)

    # B열 D열에서 전화번호 후보 추출
    phone_col_1 = excel_df.iloc[:, 1].astype(str)
    phone_col_2 = excel_df.iloc[:, 3].astype(str) if excel_df.shape[1] > 3 else ""

    # 전화번호 추출 처리
    excel_df["전화번호"] = phone_col_1.apply(clean_phone)
    excel_df["전화번호_보조"] = phone_col_2.apply(clean_phone)

    excel_df["전화번호"] = excel_df["전화번호"].replace("", excel_df["전화번호_보조"])

    # 최종 정리
    today_df = excel_df[["아이디","전화번호"]]
    today_df = today_df.drop_duplicates(subset="아이디")

    # master 누적 저장
    combined = pd.concat([master_df, today_df])
    combined = combined.drop_duplicates(subset="아이디", keep="first")

    return combined, today_df
