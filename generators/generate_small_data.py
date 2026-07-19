import os
import random

import pandas as pd
from faker import Faker

# Config constants for record limists
NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 500
NUM_ORDERS = 5000
NUM_ORDER_ITEMS = 15000
OUTPUT_DIR = "data/bronze"


# print(fake.name()) # check if it works
def create_directory(
    path: str,
) -> None:  # "-> None" it means that at the end this functions returns nothing.
    """
    Create a directory at the specified path.
    If the directory already exists, no exception is raised.
    """
    os.makedirs(
        path, exist_ok=True
    )  # exist_ok checks if this directory exists if true then skipping creation of this directory


def generate_customers(
    num_records: int, fake: Faker
) -> list[dict]:  # in this case "-> list[dict]" means that function have to return list of dictionaries
    """
    Generate a list of dictionaries, each representing a single customer.
    """
    customers = []

    # range function generate counts from 1 to NUM_CUSTOMERS include.
    for i in range(
        1, num_records + 1
    ):  # in python right side of "range" is always "opened -> )" which means that loop will stop at 999 that is why we adding +1
        # each iteration creates new dictionary
        customer = {
            "customer_id": i,
            "customer_name": fake.name(),
            "country": fake.country_code(),
            "created_at": fake.past_date(),
        }

        customers.append(customer)  # append adding new element (dict in this case) at the end of the list

    return customers  # returns new list with 1000 fake dicts


def generate_products(num_records: int) -> list[dict]:
    """
    Generate a list of dictionaries, each representing a single product.
    """
    products = []

    categories = ["Electronics", "Clothing", "Home", "Toys"]

    for i in range(1, num_records + 1):
        product = {
            "product_id": i,
            "category": random.choice(categories),
            "price": round(
                random.uniform(10.0, 1000.0), 2
            ),  # uniform generates floats instead of randint which generates only ints.
        }

        products.append(product)

    return products


def generate_orders(num_records: int, num_customers: int, fake: Faker) -> list[dict]:
    """
    Generate a list of dictionaries, each representing a single order.
    """
    orders = []

    statuses = ["Created", "Cancelled", "Awaiting delivery", "Delivered"]

    for i in range(1, num_records + 1):
        order = {
            "order_id": i,
            "customer_id": random.randint(1, num_customers),
            "order_date": fake.date_this_year(),
            "status": random.choice(statuses),
        }

        orders.append(order)

    return orders


def generate_order_items(num_records: int, num_orders: int, num_products: int) -> list[dict]:
    """
    Generate a list of dictionaries, each representing a single item from order.
    """
    order_items = []

    for i in range(1, num_records + 1):
        order_item = {
            "order_id": random.randint(1, num_orders),
            "product_id": random.randint(1, num_products),
            "quantity": random.randint(1, 10),
            "amount": round(random.uniform(1.00, 5000.0), 2),
        }

        order_items.append(order_item)

    return order_items


def save_to_parquet(data: list[dict], directory: str, filename: str) -> None:
    """
    Convert a list of dictionaries to a Panda DataFrame and save it as a Parquet file
    """

    df = pd.DataFrame(data)

    file_path = os.path.join(directory, filename)

    df.to_parquet(file_path)


def main() -> None:
    create_directory(OUTPUT_DIR)  # pass to function directory "data/bronze/"

    fake = Faker()

    print("Starting data generation...")

    customers_data = generate_customers(NUM_CUSTOMERS, fake)
    print("Generation of customers_data complete. Saving files to Parquet...")
    products_data = generate_products(NUM_PRODUCTS)
    print("Generation of products_data complete. Saving files to Parquet...")
    orders_data = generate_orders(NUM_ORDERS, NUM_CUSTOMERS, fake)
    print("Generation of orders_data complete. Saving files to Parquet...")
    order_items_data = generate_order_items(NUM_ORDER_ITEMS, NUM_ORDERS, NUM_PRODUCTS)
    print("Generation of order_items_data complete. Saving files to Parquet...")

    print("Generation complete. Saving files to Parquet...")

    save_to_parquet(customers_data, OUTPUT_DIR, "customers.parquet")
    save_to_parquet(products_data, OUTPUT_DIR, "products.parquet")
    save_to_parquet(orders_data, OUTPUT_DIR, "orders.parquet")
    save_to_parquet(order_items_data, OUTPUT_DIR, "order_items.parquet")

    print("Success: All data generated and saved successfully to the bronze layer!")


if (
    __name__ == "__main__"
):  # run main() if this file is being executed directly, not if it's being imported by another Python file.
    main()
