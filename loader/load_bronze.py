import os
import time

import duckdb
import psutil

# checking the path of this script in repo
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# move 1 level up to main folder of repo
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# build full path no matter where you run this script
BRONZE_DIR = os.path.join(PROJECT_ROOT, "data", "bronze")
DB_PATH = os.path.join(PROJECT_ROOT, "warehouse.duckdb")
TABLES = ["customers", "order_items", "orders", "products"]


def get_memory_usage() -> float:
    """
    Calculate the current memory (RAM) usage of the Python process.
    Returns the value in Megabytes (MB).
    """
    # fetching id of current process
    current_pid = os.getpid()

    # Create an object to monitor this process
    process = psutil.Process(current_pid)

    # fetching memory usage (RSS) in bytes
    memory_in_bytes = process.memory_info().rss

    # computing bytes into megabytes (MB)
    memory_in_mb = memory_in_bytes / (1024 * 1024)

    # return rounded result
    return round(memory_in_mb, 2)


def setup_database(conn: duckdb.DuckDBPyConnection) -> None:
    """
    Configure the DuckDB database connection with intentional hardware constraints
    to simulate a low-resource environment.
    """

    # Limit RAM memory for database to 200MB
    conn.execute("PRAGMA memory_limit='200MB';")

    # Limit database to use only of 2 threads of processor
    conn.execute("PRAGMA threads='2';")

    # Information about limits
    print("Database constraints applied: memory_limit-'200MB', threads=2.")


def load_single_table(conn: duckdb.DuckDBPyConnection, table_name: str) -> None:
    """Loads a single Parquet file into DuckDB."""
    file_path = f"{BRONZE_DIR}/{table_name}.parquet"
    query = f"CREATE OR REPLACE TABLE raw_{table_name} AS SELECT * FROM read_parquet('{file_path}');"
    conn.execute(query)


def load_tables(conn: duckdb.DuckDBPyConnection) -> None:
    """
    Iterate over the defined tables, load data from Parquet files into DuckDB,
    and track execution time and memory usage for each table.
    """

    for table_name in TABLES:
        # Here you can add logs of time and memory usage if you need
        load_single_table(conn, table_name)

        # create exact address of table
        file_path = f"{BRONZE_DIR}/{table_name}.parquet"

        # save beginning status (timer and usage counter)
        ram_before = get_memory_usage()
        start_time = time.time()

        # Info about loading of specific table
        print(f"Loading '{table_name}'... Current RAM: {ram_before} MB")

        # Write and send SQL query to database
        query = f"CREATE OR REPLACE TABLE raw_{table_name} AS SELECT * FROM read_parquet('{file_path}');"
        conn.execute(query)

        # Stope timer and check usage again
        end_time = time.time()
        ram_after = get_memory_usage()

        # Compute stats
        duration = end_time - start_time
        ram_diff = ram_after - ram_before

        # Summary
        print(f"Success: '{table_name}' loaded in {duration:.2f} seconds.")
        print(f"RAM after: {ram_after} MB (Difference: {ram_diff:.2f} MB). \n")


def get_db_size(db_path: str) -> None:
    """
    Check the physical file size of the database on disk.
    Prints the size in Megabytes (MB).
    """

    # check size of file (bytes)
    file_size = os.path.getsize(db_path)

    file_size_to_mb = round(file_size / (1024 * 1024), 2)
    print(f"Database file size: {file_size_to_mb} MB")


def main() -> None:
    """
    Main execution flow for the database loading process.
    """
    print("--- Process Started ---")
    print(f"Initial RAM usage: {get_memory_usage()} MB\n")

    print(f"Connecting to DuckDB database at '{DB_PATH}'...")
    conn = duckdb.connect(DB_PATH)

    # Limits config
    setup_database(conn)

    # Loading data
    load_tables(conn)

    # close connection
    conn.close()
    print("Database connection closed.")

    # check the size of saved file
    get_db_size(DB_PATH)

    # Check memory usage RAM at the end
    print(f"Final RAM usage: {get_memory_usage()} MB")
    print("---Process Finished---")


if __name__ == "__main__":
    main()
