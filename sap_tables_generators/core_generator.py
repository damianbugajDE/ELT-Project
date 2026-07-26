import pandas as pd
import numpy as np

def upload_dataframe_to_bronze(df: pd.DataFrame, bucket_name: str, table_name: str) -> None:
    """
    Save dataframe as parquet file in bronze layer on S3
    """
    file_path = f"s3://{bucket_name}/bronze/sap/{table_name}/{table_name}.parquet"

    print(f"Loading {len(df)} wierszy do {file_path}...")

    # Pandas automatically will use s3fs to manage the path s3:// and credentials from ~/.aws/credentials
    df.to_parquet(file_path, index=False, engine="pyarrow")

    print(f"Table {table_name} has been loaded successfully!")

def inject_defects(df: pd.DataFrame, ratio: float, numeric_col: str = None) -> pd.DataFrame:
    """
    Injects defects to data frame to cause issues with data quality.
    It simulates errors from source which should be cleaned in further layer in dbt
    """
    if ratio <= 0 or len(df) == 0:
        return df

    # Copying DataFrame, to not overwrite original object (good practice)
    df_dirty = df.copy()

    # Set how much rows should be affected
    num_dirty = int(len(df_dirty) * ratio)
    dirty_indices = np.random.choice(df_dirty.index, num_dirty, replace=True)

    # 1. We're ruining the customer ID in SAP (MANDT) to negative/unknown (e.g. "-1")
    if "MANDT" in df_dirty.columns:
        mandt_indices = np.random.choice(dirty_indices, size=len(dirty_indices) // 2, replace=False)
        df_dirty.loc[mandt_indices, "MANDT"] = "-1"

    # 2. We generate lack of data (NaN) in key numeric column (e.g. NETWR)
    if numeric_col and numeric_col in df_dirty.columns:
        amount_indices = np.random.choice(dirty_indices, size=len(dirty_indices) // 4, replace=False)
        df_dirty.loc[amount_indices, numeric_col] = np.nan

    return df_dirty
