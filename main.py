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
    run_loading()  # Flow tylko wywołuje taska


if __name__ == "__main__":
    # Używamy serve, aby "wystawić" przepływ do Prefect Cloud
    main.serve(name="elt-bronze-deployment")
