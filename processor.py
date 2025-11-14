def update_master(excel_df, optimal_df):
    excel_df = excel_df.rename(columns={
        excel_df.columns[0]: "블로그ID",
        excel_df.columns[1]: "제목",
        excel_df.columns[3]: "전화번호"
    })

    # 문자열 원본 그대로 유지
    excel_df["블로그ID"] = excel_df["블로그ID"].astype(str)

    # master 파일 로드
    master_df = load_master()

    # merge
    combined_df = pd.concat([master_df, excel_df], ignore_index=True)

    # 완전히 동일한 문자열만 중복 제거
    combined_df = combined_df.drop_duplicates(subset=["블로그ID"], keep="first")

    # 저장
    combined_df.to_csv("master_storage.csv", index=False, encoding="utf-8-sig")

    return combined_df, excel_df
