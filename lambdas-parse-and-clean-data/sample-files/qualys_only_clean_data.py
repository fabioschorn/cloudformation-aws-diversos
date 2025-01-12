#!/usr/bin/env python3
import csv

def process_qualys_csv(input_file_path, output_file_path):
    """
    Reads a Qualys CSV file and does the following:
    1. Skips the first 8 lines (often report headers).
    2. Parses the CSV (semicolon delimiter).
    3. Extracts IP, DNS, CVE ID, QID, and Severity columns.
    4. Removes duplicate (QID) rows for the same IP.
    5. Writes a new CSV grouping QIDs under each IP address other columns of item 3 above.
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
        #    IP, DNS, CVE ID, QID, Severity

        for row in reader:
            ip = row.get('IP', '').strip()
            dns = row.get('DNS', '').strip()
            cve = row.get('CVE ID', '').strip()
            qid = row.get('QID', '').strip()
            severity = row.get('Severity', '').strip()

            # Skip rows with missing IP or QID
            if not ip or not qid:
                continue

            # Add the QID and Severity to the set for this IP
            if ip not in data_dict:
                data_dict[ip] = set()
            data_dict[ip].add((qid, severity))

    # Write the processed data to a new CSV file
    with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['IP', 'DNS', 'CVE ID', 'QID', 'Severity'])

        for ip, qid_severity_set in data_dict.items():
            for qid, severity in qid_severity_set:
                writer.writerow([ip, '', '', qid, severity
                ])

    print(f"Done! Processed data written to '{output_file_path}'.")
    return output_file_path

if __name__ == "__main__":
    # Example usage:
    input_csv = "qualys_report.csv"    # Change to your actual input file
    output_csv = "qualys_report_output.csv"         # Change to your desired output file
    process_qualys_csv(input_csv, output_csv)