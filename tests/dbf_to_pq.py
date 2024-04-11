from dbfread import DBF
import pandas as pd

def dbf_to_csv(dbf_file, csv_file, chunk_size=100000):
    # Open the DBF file for reading
    with DBF(dbf_file, encoding='utf-8') as dbf_reader:
        # Open the CSV file for writing
        with open(csv_file, 'w', encoding='utf-8') as csv_writer:
            # Write the header row
            header_written = False
            for record in dbf_reader:
                if not header_written:
                    csv_writer.write(','.join(record.keys()) + '\n')
                    header_written = True
                
                # Write each record to the CSV file
                csv_writer.write(','.join(map(str, record.values())) + '\n')

# Example usage:
dbf_file = './downloaded_files/SHP_KATASTRIYKSUS.dbf'
csv_file = './downloaded_files/output.csv'
dbf_to_csv(dbf_file, csv_file)