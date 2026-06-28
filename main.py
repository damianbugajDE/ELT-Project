import duckdb

from loader.load_bronze import load_tables
from prefect import flow, task

# DB_PATH should be defined in one place
DB_PATH = "warehouse.duckdb"


@task(name="Load Bronze Tables")
def run_loading():
    with duckdb.connect(DB_PATH) as conn:
        load_tables(conn)


@flow(name="ELT Bronze Flow")
def main():
    print("Running process ELT in refect Cloud!")
    run_loading()


if __name__ == "__main__":
    main()
