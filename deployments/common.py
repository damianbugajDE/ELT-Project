import os   
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

from sap_tables_generators.core_generator import upload_dataframe_to_bronze
from sap_tables_generators.definitions import generate_fake_sap_sales