import pandas as pd
import os

main_csv_file = "combined_data.csv"
all_files = [f for f in os.listdir(".") if f.endswith(".csv") and f != main_csv_file]

main_df = pd.read_csv(main_csv_file)
main_df["Topics"] = main_df["Topics"].fillna("")

for csv_file in all_files:
    print(f"Processing file: {csv_file}")
    other_df = pd.read_csv(csv_file)

    merged_df = pd.merge(other_df, main_df[["ID", "Topics"]], on="ID", how="left")
    merged_df.to_csv(csv_file, index=False)

print("All files updated with Topics data!")
