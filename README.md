# 🚀 ELT Pipeline: Faker to DuckDB

This project is a fully automated ELT (Extract, Load, Transform) data pipeline written in Python. It simulates the process of generating millions of e-commerce records (Customers, Products, Orders, Order Items), saving them to compressed Parquet files, and then loading them into a **DuckDB** analytical database using constrained system resources.

The project was built following **SOLID** and **KISS** principles.

## 🛠 Tech Stack & Tools
* **Python 3.10+**
* **Package Manager:** `uv` (a blazingly fast alternative to pip)
* **Data Generation:** `Faker`
* **Processing & Formatting:** `pandas`, `pyarrow` (Parquet)
* **Database:** `DuckDB`
* **Linter/Formatter:** `Ruff` (configured to 120 line length in `pyproject.toml`)

---

## ⚙️ Quick Start (Installation)

Follow the instructions below to get the project up and running on your local machine.

### 1. Clone the repository
Open your terminal and download the code:
```bash
git clone https://github.com/damianbugajDE/ELT-Project
cd elt-project
```

### 2. Install the uv package manager (if you don't have it)
This project uses uv for lightning-fast dependency management. If it's not installed yet, use the following command:

Mac/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`

Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

### 3. Create the environment and install dependencies
Thanks to the pyproject.toml and uv.lock files, recreating the exact environment takes just one command. In the project root directory, run:

`uv sync`

### 4. Activate the virtual environment
To run the scripts, you need to activate the created environment:

# Windows: 
`.venv\Scripts\activate`

# Mac/Linux: 
`source .venv/bin/activate`

### 🚀 Running the Data Pipeline
The pipeline execution consists of two main steps.

## Step 1: Generate raw data (Extract)
Run the first script to generate mock e-commerce data and save it as optimized .parquet files in the data/bronze/ directory.

`python generate_data.py`

## Step 2: Load data into the data warehouse (Load)
Run the second script, which will create a warehouse.duckdb database file and load the previously generated Parquet files into it.

# Note: The script intentionally imposes bottlenecks on the database (memory_limit='200MB', threads=2) to simulate a low-resource environment and actively monitors RAM usage during the process.

`python load_data.py`

### 📂 Directory Structure
After fully running the project, the file structure will look like this:

``` bash
elt-project/
├── .venv/                  # Virtual environment (git ignored)
├── data/
│   └── bronze/             # Generated .parquet files (git ignored)
├── generate_data.py        # Script 1: Data generator
├── load_data.py            # Script 2: Load data to DuckDB
├── warehouse.duckdb        # Physical database file (created after running Step 2)
├── pyproject.toml          # Project configuration and Ruff rules
├── uv.lock                 # Locked exact dependency versions
└── README.md               # This file

```
