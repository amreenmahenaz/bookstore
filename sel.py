with open(csv_file_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)  # Use DictReader to access columns by name
    for row in reader:
        # Extract values from the current row
        key = row["key"]
        content_vector = row["content_vector"]
        source = row["source"]
        content = row["content"]
        active = row["active"]
