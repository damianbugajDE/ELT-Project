import duckdb

from loader.load_bronze import load_tables
from prefect import flow, task

DB_PATH = "warehouse.duckdb"


@task(name="Load Bronze Tables")
def run_loading():
    with duckdb.connect(DB_PATH) as conn:
        load_tables(conn)


@flow(name="ELT Bronze Flow")
def main():
    print("Starting ELT process...")
    run_loading()  # Flow calls task only


if __name__ == "__main__":
    # Use serve to present flow to Prefect Cloud
    main.serve(name="elt-bronze-deployment")
