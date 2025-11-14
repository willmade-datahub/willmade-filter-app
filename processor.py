import pandas as pd

MASTER_FILE = "storagemaster_list.csv"

def load_master():
    try:
        return pd.read_csv(MASTER_FILE)
    except:
        return pd.DataFrame(columns=["블로그 ID", "전화번호"])

def save_master(df):
    df.to_csv(MASTER_FILE, index=False)

def update_master(excel_df, optimal_df):
    master_df = load_master()

    excel_df.columns = ["블로그 ID", "전화번호"]

    selected_df = excel_df[excel_df["블로그 ID"].isin(optimal_df["블로그 ID"])]

    updated_master = pd.concat([master_df, selected_df], ignore_index=True)
    updated_master.drop_duplicates(subset="블로그 ID", keep="first", inplace=True)

    save_master(updated_master)

    return updated_master, excel_df, selected_df
