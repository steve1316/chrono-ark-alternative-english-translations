import csv

def merge_csv(primary_file: str, secondary_file: str, output_file: str):
    """Merges two CSV files and writes the result to a new file.
    
    Args:
        primary_file (str): The path to the primary CSV file (exported from within Chrono Ark).
        secondary_file (str): The path to the secondary CSV file (the mod's initial translation file).
        output_file (str): The path to the final CSV file.
    """
    with open(primary_file, mode="r", encoding="utf-8-sig") as p_file, open(secondary_file, mode="r", encoding="utf-8-sig") as s_file:
        primary_reader = csv.DictReader(p_file)
        secondary_reader = csv.DictReader(s_file)
        
        # Print the headers.
        print(primary_reader.fieldnames)
        print(secondary_reader.fieldnames)
        
        primary_rows = list(primary_reader)
        secondary_data = {row["Key"]: row for row in secondary_reader}
        
        fieldnames = primary_reader.fieldnames
        
        with open(output_file, mode="w", encoding="utf-8-sig", newline="") as out_file:
            writer = csv.DictWriter(out_file, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in primary_rows:
                print("Processing row: ", row["Key"])
                key = row["Key"]
                if key in secondary_data:
                    print("Primary headers: ", list(row.keys()))
                    print("Secondary headers: ", list(secondary_data[key].keys()))
                    merged_row = secondary_data[key]
                else:
                    merged_row = row.copy()
                    if merged_row["English"] and row["Chinese"] == "" and row["Korean"] == "" and row["Japanese"] == "" and row["Chinese-TW [zh-tw]"] == "":
                        merged_row["Chinese"] = merged_row["English"]
                        merged_row["English"] = "#TODO"

                writer.writerow(merged_row)

if __name__ == "__main__":
    primary_file = "primary.csv"
    secondary_file = "secondary.csv"
    output_file = "result.csv"
    merge_csv(primary_file, secondary_file, output_file)