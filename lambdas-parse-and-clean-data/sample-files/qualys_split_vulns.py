#!/usr/bin/env python3
import csv

def process_qualys_csv(input_file_path, output_pci_file, output_nonpci_file):
    """
    Reads a Qualys CSV file and does the following:
    1. Skips the first 8 lines (often report headers).
    2. Parses the CSV (semicolon delimiter).
    3. Keeps only these columns (in this order):
       IP, DNS, OS, QID, Title, Severity, CVE ID, Vendor Reference,
       Threat, Impact, Solution, PCI Vuln, Category
    4. Writes two CSV files:
       - One for rows where 'PCI Vuln' == 'yes' (case-insensitive).
       - One for rows where 'PCI Vuln' == 'no' (or anything else).
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
        
        # Parse the remaining lines as CSV with semicolon delimiter
        reader = csv.DictReader(infile, delimiter=';')
        
        # Prepare two output files
        with open(output_pci_file, 'w', newline='', encoding='utf-8') as pci_out, \
             open(output_nonpci_file, 'w', newline='', encoding='utf-8') as nonpci_out:
             
            # Create separate writers
            pci_writer = csv.DictWriter(pci_out, fieldnames=wanted_columns)
            nonpci_writer = csv.DictWriter(nonpci_out, fieldnames=wanted_columns)
            
            # Write headers
            pci_writer.writeheader()
            nonpci_writer.writeheader()
            
            # Process each row
            for row in reader:
                # Build a new dict containing only the wanted columns
                filtered_row = {}
                for col in wanted_columns:
                    filtered_row[col] = row.get(col, '').strip()
                
                # Check the PCI Vuln column
                pci_value = filtered_row["PCI Vuln"].lower()
                
                if pci_value == "yes":
                    pci_writer.writerow(filtered_row)
                else:
                    # If it's "no" or anything else, treat as non-PCI
                    nonpci_writer.writerow(filtered_row)

    print(f"Done! Processed data written to '{output_pci_file}' (PCI) and '{output_nonpci_file}' (non-PCI).")


if __name__ == "__main__":
    # Example usage:
    input_csv = "qualys_report.csv"        # The original Qualys CSV
    output_pci_csv = "output_pci.csv"      # Rows with PCI Vuln == "yes"
    output_nonpci_csv = "output_non-pci.csv"  # Rows with PCI Vuln != "yes"

    process_qualys_csv(input_csv, output_pci_csv, output_nonpci_csv)