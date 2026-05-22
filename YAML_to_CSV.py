import os
import yaml
import pandas as pd

# =========================
# PATHS
# =========================
INPUT_FOLDER = r"D:\Guvi\Projects\Stock-Analytics\Stock_Explore"
OUTPUT_FOLDER = r"D:\Guvi\Projects\Stock-Analytics\Stock_Trial_CSV"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Dictionary: { "SBIN": [df1, df2, ...], "TCS": [...] }
stock_data = {}

# =========================
# READ ALL YAML FILES
# =========================
for month_folder in os.listdir(INPUT_FOLDER):
    month_path = os.path.join(INPUT_FOLDER, month_folder)

    if not os.path.isdir(month_path):
        continue

    for file in os.listdir(month_path):
        if not file.endswith((".yaml", ".yml")):
            continue

        file_path = os.path.join(month_path, file)

        with open(file_path, "r", encoding="utf-8") as f:
            records = yaml.safe_load(f)

        if not records or not isinstance(records, list):
            continue

        for record in records:
            ticker = record.get("Ticker")   # CORRECT KEY

            if not ticker:
                continue

            df = pd.DataFrame([record])

            if ticker not in stock_data:
                stock_data[ticker] = [df]
            else:
                stock_data[ticker].append(df)

# =========================
# SAVE ONE CSV PER STOCK
# =========================
for ticker, df_list in stock_data.items():
    final_df = pd.concat(df_list, ignore_index=True)

    # Optional: sort by date
    if "date" in final_df.columns:
        final_df["date"] = pd.to_datetime(final_df["date"])
        final_df = final_df.sort_values("date")

    csv_path = os.path.join(OUTPUT_FOLDER, f"{ticker}.csv")
    final_df.to_csv(csv_path, index=False)

print(f"Successfully created {len(stock_data)} stock CSV files")
print(f"Output folder: {OUTPUT_FOLDER}")