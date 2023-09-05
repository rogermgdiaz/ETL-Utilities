import psycopg2
import os
from tqdm import tqdm

# Database configuration (adjust it for your environment)
db_config = {
    "host": "your_host",
    "database": "your_database",
    "user": "your_user",
    "password": "your_password"
}

# Full path to the directory containing the divided SQL files
divided_files_directory = "path_to_your_files"

# Get the list of SQL files in the directory
sql_files = [file for file in os.listdir(divided_files_directory) if file.endswith(".sql")]

# Sort the files by name
sql_files.sort()

# Connect to the database
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("BEGIN;")

    # Iterate over the files and execute SQL queries with a progress bar
    for sql_file in tqdm(sql_files, desc="Inserting data"):
        file_path = os.path.join(divided_files_directory, sql_file)
        with open(file_path, "r") as file:
            sql_query = file.read()
            cursor.execute(sql_query)

    cursor.execute("COMMIT;")
    conn.commit()
    print("Data insertion successful.")

except psycopg2.Error as e:
    print(f"Error inserting data into the database: {e}")

finally:
    cursor.close()
    conn.close()

print("Process completed.")
