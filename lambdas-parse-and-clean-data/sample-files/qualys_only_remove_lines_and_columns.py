#!/usr/bin/env python3
import csv

def process_qualys_csv(input_file_path, output_file_path):
    """
    Reads a Qualys CSV file and does the following:
    1. Skips the first 8 lines (often report headers).
    2. Parses the CSV (semicolon delimiter).
    3. Keeps only these columns (in this order):
       IP, DNS, OS, QID, Title, Severity, CVE ID, Vendor Reference,
       Threat, Impact, Solution, PCI Vuln, Category
    4. Writes a new CSV file with just these columns.
    """

    # Define the columns we want to keep
    wanted_columns = [
        "IP",
        "DNS",
        "OS",
        "QID",
        "Title",
        "Severity",
        "CVE ID",
        "Vendor Reference",
        "Threat",
        "Impact",
        "Solution",
        "PCI Vuln",
        "Category"
    ]

    with open(input_file_path, 'r', encoding='utf-8') as infile:
        # Skip the first 8 lines
        for _ in range(8):
            next(infile, None)
        
        # Now parse the remaining lines as CSV with semicolon delimiter
        reader = csv.DictReader(infile, delimiter=';')
        
        # Create the output CSV
        with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=wanted_columns)
            writer.writeheader()
            
            for row in reader:
                # Build a new dict containing only the wanted columns
                filtered_row = {}
                for col in wanted_columns:
                    # Use row.get(col, '') to avoid KeyError if column missing
                    filtered_row[col] = row.get(col, '').strip()
                
                writer.writerow(filtered_row)

    print(f"Done! Processed data (only the required columns) written to '{output_file_path}'.")


if __name__ == "__main__":
    # Example usage:
    input_csv = "qualys_report.csv"   # Change to your actual input file
    output_csv = "output.csv"         # Desired output file
    process_qualys_csv(input_csv, output_csv)