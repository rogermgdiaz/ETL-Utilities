# ETL-Utilities
A toolkit for efficient data ETL – scripts, automation, and more to supercharge data integration.

This repository contains two Python scripts that are part of an ETL (Extract, Transform, Load) utility for working with SQL data. The scripts are used to perform the following tasks:

## `cargue_archivos.py`

`cargue_archivos.py` is a script used for inserting data into a PostgreSQL database. It connects to a local PostgreSQL database and inserts data from SQL files located in a specified directory.

### Prerequisites

Before running the script, make sure you have the following prerequisites installed:

- Python 3
- psycopg2 library
- tqdm library

### Usage

1. Modify the `db_config` dictionary in the script to specify your PostgreSQL database connection details.

2. Ensure that your SQL files are located in the `archivos_fragmentados` directory.

3. Run the script using the following command:
 
'py cargue_archivos.py'

The script will insert data from the SQL files into your database.

## `divisor_sql.py`

`divisor_sql.py` is a script used for splitting a large SQL file into smaller files. It takes an SQL file with multiple `INSERT` statements and divides it into smaller files with a specified maximum number of statements per file.

### Usage

1. Place your original SQL file (`postgres_public_trades.sql`) in the same directory as this script.

2. Run the script using the following command:
'py divisor_sql.py'

