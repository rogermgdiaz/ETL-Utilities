import os
import re

# Original SQL file name
original_sql_file = "postgres_public_trades.sql"

# Prefix for divided files
divided_files_prefix = "fragment_sql_"

# Maximum number of INSERT statements per fragment
max_statements_per_fragment = 10000

# Read the content of the original SQL file
with open(original_sql_file, "r") as original_file:
    content = original_file.read()

# Split the structure from the values insertion
structure, values = re.split(r"\);\s*", content, maxsplit=1)
structure += ");"  # Add the closing parenthesis that was lost during the split

# Split the values into individual lines
value_lines = values.split("\n")
value_lines = [line.strip() for line in value_lines if line.strip()]  # Remove empty lines

# Divide the content into fragments based on the maximum number of statements
fragments = [value_lines[i:i + max_statements_per_fragment] for i in range(0, len(value_lines), max_statements_per_fragment)]

# Replace the last comma (,) with a semicolon (;) in each fragment
for fragment in fragments:
    fragment[-1] = fragment[-1].rstrip(",") + ";"

# Directory where the divided SQL files will be saved
destination_directory = "divided_files"

# Create the directory if it doesn't exist
os.makedirs(destination_directory, exist_ok=True)

# Create SQL fragment files with the INSERT structure
for i, fragment in enumerate(fragments):
    fragment_file_name = os.path.join(destination_directory, f"{divided_files_prefix}{i + 1}.sql")
    
    # If it's not the first fragment, add the INSERT statement
    if i != 0:
        with open(fragment_file_name, "w") as fragment_file:
            fragment_file.write(f"INSERT INTO public.trades (country_code, year, comm_code, flow, trade_usd, kg, quantity, quantity_name) VALUES\n")
            fragment_file.write("\n".join(fragment))
            fragment_file.write("\n")  # Add a new line
    else:
        # The first fragment contains the table structure and doesn't need the INSERT statement
        with open(fragment_file_name, "w") as fragment_file:
            fragment_file.write(structure + "\n")
            fragment_file.write("\n".join(fragment))
            fragment_file.write("\n")  # Add a new line

print("Divided files created successfully.")
