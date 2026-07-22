import argparse
import io
from datetime import datetime
import boto3

import pyarrow as pa
import pyarrow.parquet as pq

from generators.data_engine import create_chunk, inject_defects

CHUNK_SIZE = 500_000


def main(total_rows: int, dirty_ratio: float, source_name: str, category: str = "big") -> None:
    print(f"Start generating {total_rows} rows for {source_name}...")

    # Dynamic name: e.g. "sap_sales_20260705_1385.parquet"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{source_name}_{timestamp}.parquet"
    
    # Ścieżka docelowa w S3 (zgodna z warstwą Bronze)
    bucket_name = "elt-project-data-foundry-lake"
    file_key = f"bronze/{category}/{filename}"

    # Bufory do zapisu Parquet w pamięci RAM (zamiast dysku lokalnego)
    parquet_buffer = io.BytesIO()
    writer = None

    # Generowanie danych w pętli (chunkach)
    for i in range(0, total_rows, CHUNK_SIZE):
        size = min(CHUNK_SIZE, total_rows - i)

        # Użycie silnika danych
        df = create_chunk(size, start_id=i)
        df = inject_defects(df, dirty_ratio)

        # Konwersja DataFrame na tabelę pyarrow
        table = pa.Table.from_pandas(df)

        if writer is None:
            # Pierwszy chunk: inicjalizacja writera do bufora w pamięci
            writer = pq.ParquetWriter(parquet_buffer, table.schema)
        
        writer.write_table(table)
        print(f"Processed {i + size} / {total_rows} rows.")

    if writer:
        writer.close()  # Zamknięcie writera po zakończeniu pętli

    # Przygotowanie bufora do wysyłki (przesunięcie wskaźnika na początek)
    parquet_buffer.seek(0)

    # Wysyłka strumienia bezpośrednio do AWS S3
    print(f"Uploading to S3 bucket '{bucket_name}' at '{file_key}'...")
    s3_client = boto3.client("s3")
    s3_client.upload_fileobj(parquet_buffer, bucket_name, file_key)
    
    print(f"Generation complete. Data successfully uploaded to s3://{bucket_name}/{file_key}")

    """
    NOTE: Why use Parquet in-memory buffer with S3?
    
    1. Streamlined Cloud Upload: By using io.BytesIO, we retain all 
       the columnar efficiency and schema enforcement of Parquet 
       without writing temporary files to the local disk/repository.
       
    2. Chunking Safety: Even with millions of rows, processing in 
       chunks keeps local memory consumption stable while building 
       a valid, atomic Parquet file stream for S3.
    """


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generator Big Data to S3")
    parser.add_argument("--total-rows", type=int, default=1_000_000, help="Overall count of rows")
    parser.add_argument("--dirty-ratio", type=float, default=0.05, help="% of errors (e.g. 0.05 for 5%)")
    parser.add_argument("--source-name", type=str, default="sap_sales", help="Source system name")
    parser.add_argument("--category", type=str, default="big", help="Data category folder")

    args = parser.parse_args()

    main(args.total_rows, args.dirty_ratio, args.source_name, args.category)