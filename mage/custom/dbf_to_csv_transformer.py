from dbfread import DBF


def dbf_to_csv(dbf_file, csv_file):
    # Open the DBF file for reading
    print("opening the dbf file")
    with DBF(dbf_file, encoding='utf-8') as dbf_reader:
        # Open the CSV file for writing
        print("opening the csv file")
        with open(csv_file, 'w', encoding='utf-8') as csv_writer:
            # Write the header row
            header_written = False
            for record in dbf_reader:
                if not header_written:
                    csv_writer.write(';'.join(record.keys()) + '\n')
                    header_written = True
                
                # TRANSFORMATINS
                # Replace 'None' with empty string only for MAX_HIND column and write record
                # replace ',' with ';' as the delimiter (to avoid cases where it is used in comment fields)
                for key, value in record.items():
                    if key == 'MAX_HIND' and value == 'None':
                        record[key] = ''
                    elif key == 'MARKETEKST' and value == '-':
                        record[key] = ''
                    else:
                        record[key] = str(value).replace(';', ',') if value is not None else ''
                
                csv_writer.write(';'.join(record.values()) + '\n')

@custom
def transform_custom(dbf_file: str, *args, **kwargs):
    print(f"DBF file path received: {dbf_file}")
    csv_file = './downloaded_files/KATASTRIYKSUS.csv'
    dbf_to_csv(dbf_file, csv_file)

    return csv_file


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
