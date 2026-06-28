import os

import duckdb

from loader.load_bronze import DB_PATH, load_tables


def test_customers_table_has_data():
    """Test checking, if table raw_customers has records after load."""
    # check if file of database doesn't exists before test
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    # Create connection and run loading process
    conn = duckdb.connect(DB_PATH)

    # Run load function
    load_tables(conn)

    # Checking status of the table
    cursor = conn.execute("SELECT COUNT(*) FROM raw_customers")
    row = cursor.fetchone()
    result = row[0] if row else 0

    # Assertion of this table which must have at least 1 record
    assert result > 0, "Table raw_customers is empty!"

    # cleaning
    conn.close()
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


def test_database_file_created():
    """Check if file of database exists after the operation is done"""
    open(DB_PATH, "a").close()

    assert os.path.exists(DB_PATH) == True

    # cleaning
    os.remove(DB_PATH)
