import argparse
import os
from datetime import datetime

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from .data_engine import create_chunk, inject_defects

CHUNK_SIZE = 500_000


def main(total_rows: int, dirty_ratio: float, source_name: str, category="big") -> None:
    print(f"Start generating {total_rows} rows...")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    # path to save created file
    output_dir = os.path.join(PROJECT_ROOT, "data", "bronze", category)

    os.makedirs(output_dir, exist_ok=True)

    # Dynamic name: e.g. "sap_sales_20260705_1385.parquet"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{source_name}_{timestamp}.parquet"
    output_path = os.path.join(output_dir, filename)

    print(f"Generating date for {source_name} into {output_path}...")

    # writer of parquet files
    writer = None

    # Generating data in loop (chunks)
    for i in range(0, total_rows, CHUNK_SIZE):
        size = min(CHUNK_SIZE, total_rows - i)

        # Using data_engine script
        df = create_chunk(size, start_id=i)
        df = inject_defects(df, dirty_ratio)

        # Convert DataFrame to pyarrow table
        table = pa.Table.from_pandas(df)

        if writer is None:
            # First chunk: initialize writer
            writer = pq.ParquetWriter(output_path, table.schema)
        writer.write_table(table)
        print(f"Saved {i + size} / {total_rows} rows.")

    if writer:
        writer.close()  # Close file after the loop has been finished.
    print(f"Generation complete.Data saved to {output_path}")

    """
    NOTE: Why use Parquet over CSV mode='a'?
    
    1. Columnar Efficiency: Parquet stores data column-wise, not row-wise. 
       This is highly optimized for analytical engines like DuckDB, allowing 
       it to read only specific columns (e.g., 'value') without scanning the 
       entire dataset.
       
    2. Schema Enforcement: Using pyarrow ensures data consistency. If a 
       data chunk accidentally changes its type (e.g., from int to string), 
       pyarrow will raise an error, providing a critical safety net during 
       the ELT process.
       
    3. Robust Writing: CSV 'append' mode is prone to data corruption if the 
       script crashes mid-write. ParquetWriter manages data in structured 
       'row groups', making the write process atomic, safe, and resilient 
       to interruptions.
    """


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generator Big Data")
    parser.add_argument("--total-rows", type=int, default=1_000_000, help="Overall count of rows")
    parser.add_argument("--dirty-ratio", type=float, default=0.05, help="% of errors (e.g. 0.005 for 5%)")
    parser.add_argument("--source-name", type=str, default="sap_sales", help="Source system name")
    parser.add_argument("--output-file", type=str, default="data.parquet", help="Name of the exit file")

    args = parser.parse_args()

    main(args.total_rows, args.dirty_ratio, args.source_name)
