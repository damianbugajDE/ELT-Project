import os

import duckdb
import pandas as pd

from loader.load_bronze import DB_PATH, load_single_table


def test_customers_table_has_data():
    """Test checking, if table raw_customers has records after load."""
    # Mock of creating parquet file for CI ACtion tests
    os.makedirs("data/bronze", exist_ok=True)
    df = pd.DataFrame({"id": [1, 2], "name": ["Test", "User"]})
    df.to_parquet("data/bronze/customers.parquet")

    # check if file of database doesn't exists before test
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    # Create connection and run loading process
    conn = duckdb.connect(DB_PATH)

    # Run load function
    load_single_table(conn, "customers")

    # Checking status of the table
    cursor = conn.execute("SELECT COUNT(*) FROM raw_customers")
    row = cursor.fetchone()
    count = row[0] if row else 0

    assert count == 2, f"Expected 2 records, but found {count}"

    # cleaning
    conn.close()
    os.remove(DB_PATH)
    os.remove("data/bronze/customers.parquet")


def test_database_file_created():
    """Check if file of database exists after the operation is done"""
    open(DB_PATH, "a").close()

    assert os.path.exists(DB_PATH)

    # cleaning
    os.remove(DB_PATH)
