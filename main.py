import duckdb

from loader.load_bronze import load_tables
from prefect import flow, task

# DB_PATH powinno być zdefiniowane w jednym, wspólnym miejscu
DB_PATH = "warehouse.duckdb"


@task
def run_loading():
    with duckdb.connect(DB_PATH) as conn:
        load_tables(conn)


@flow(name="ELT Bronze Flow")
def main():
    print("Uruchamiam proces ELT w Prefect Cloud!")
    run_loading()


if __name__ == "__main__":
    main()
