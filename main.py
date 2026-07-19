import os

import duckdb

from generators.generate_big_data import main as generate_data
from loader.load_bronze import load_tables
from prefect import flow, task

DB_PATH = "warehouse.duckdb"


@task(name="Generate Raw Data")
def run_generator(rows: int, ratio: float, source: str):
    """Task which generates parquet files in data/bronze/"""
    generate_data(rows, ratio, source)
    return "Data generated"


@task(name="Load Bronze Tables")
def run_loading():
    with duckdb.connect(DB_PATH) as conn:
        load_tables(conn)


@flow(name="ELT Bronze Flow")
def main_flow(rows: int = 1000000, ratio: float = 0.05):
    print("Starting ELT process...")

    # Data generating
    status = run_generator(rows, ratio, "sap_sales")
    print(status)

    # Loading to DuckDB
    run_loading()  # Flow calls task only
    print("ELT process finished successfully!")


if __name__ == "__main__":
    # Use serve to present flow to Prefect Cloud
    main_flow.serve(name="elt-bronze-deployment")
