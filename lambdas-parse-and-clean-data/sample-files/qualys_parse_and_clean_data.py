#!/usr/bin/env python3

import csv

def process_qualys_csv(input_file_path, output_file_path):
    """
    Reads a Qualys CSV file and does the following:
    1. Skips the first 8 lines (often report headers).
    2. Parses the CSV (semicolon delimiter).
    3. Extracts IP, QID, and Severity columns.
    4. Removes duplicate (IP, QID) pairs.
    5. Writes a new CSV grouping QIDs under each IP with their severity.
    """

    # We'll store data in a dictionary:
    #    data_dict = { ip_address: set((qid, severity), ...) }
    data_dict = {}

    with open(input_file_path, 'r', encoding='utf-8') as infile:
        # Skip the first 8 lines (report headers or disclaimers)
        for _ in range(8):
            next(infile, None)
        
        # Now use csv.DictReader with semicolon as the delimiter
        reader = csv.DictReader(infile, delimiter=';')
        
        # The DictReader will map each column name to its respective field 
        # (according to the row's position).
        # We expect these columns to be present:
        #   IP, DNS, NetBIOS, OS, IP Status, QID, Title, Type, Severity, Port, 
        #   Protocol, FQDN, SSL, CVE ID, Vendor Reference, Bugtraq ID,
        #   Threat, Impact, Solution, Exploitability, Associated Malware,
        #   Results, PCI Vuln, Instance, Category
        # We'll extract only IP, QID, Severity.

        for row in reader:
            ip = row.get('IP', '').strip()
            qid = row.get('QID', '').strip()
            severity = row.get('Severity', '').strip()
            
            if not ip or not qid:
                # If we don't have IP or QID, skip
                continue
            
            # Insert into our dictionary
            if ip not in data_dict:
                data_dict[ip] = set()
            
            # We store the (QID, Severity) tuple to allow grouping by IP
            data_dict[ip].add((qid, severity))

    # Now write the output CSV with columns: IP, QID, Severity
    with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['IP', 'QID', 'Severity']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # For each IP, we output each unique (QID, Severity)
        for ip, qid_sev_set in data_dict.items():
            for (qid, severity) in qid_sev_set:
                writer.writerow({
                    'IP': ip,
                    'QID': qid,
                    'Severity': severity
                })

    print(f"Done! Processed data written to '{output_file_path}'.")


if __name__ == "__main__":
    # Example usage:
    input_csv = "qualys_report.csv"    # Change to your actual input file
    output_csv = "output.csv"         # Change to your desired output file
    process_qualys_csv(input_csv, output_csv)