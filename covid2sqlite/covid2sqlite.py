import csv
import sqlite3
import sys
from datetime import datetime
from typing import List, Optional

import requests


class Covid2Sqlite():
    """Download a CSV file from an URL and store it into a SQLite database."""
    
    csv_source_url: str = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        
    def get_csv_file(self, csv_file_url: Optional[str]=None) -> str:
        """Retrieves a CSV file from an URL.

        Args:
            csv_file_url (Optional[str], optional): CSV file's URL. If not provided, use the default URL: https://opendata.ecdc.europa.eu/covid19/casedistribution/csv. Defaults to None.

        Returns:
            str: Returns the downloaded file's name.
        """        
        csv_destination_filename = "covid_report_" + datetime.utcnow().strftime("%Y_%m_%d") + ".csv"
        if csv_file_url:
            self.csv_source_url = csv_file_url
        if self.verbose :
                print("Getting CSV file from URL: {}".format(self.csv_source_url))
        try:
            req = requests.get(self.csv_source_url)
            url_content = req.content
            csv_destination = open(csv_destination_filename, 'wb')
            csv_destination.write(url_content)
            csv_destination.close()
            if self.verbose :
                print("CSV file saved as: {}".format(csv_destination_filename))
            return csv_destination_filename
        except:
            print('Error while retrieving the CSV file. ', sys.exc_info()[1])
            print()
            return None
        
    def save_csv_to_sqlite(self, csv_filename: str, sqlite_db_name: str = "covid.db", table_name:str = "covid", table_primary_keys: Optional[List[str]] = None) -> bool:
        """Creates a SQLite database and upload the CSV file into it.
        
        Gets the header of the CSV file and create the database's table column names.

        Args:
            csv_filename (str): CSV filename.
            sqlite_db_name (str, optional): Destination database. Defaults to "covid.db".
            table_name (str, optional): Destination table in the database. Defaults to "covid".
            table_primary_keys (Optional[List[str]], optional): Columns to keep as primary keys. Defaults to None.

        Returns:
            bool: Returns True if the loading into the database is successful.
        """        
        if csv_filename:
            table_pk: str = ''
            csv_filename.encode('utf-8')
            csv_header = self.get_csv_header(csv_filename)
            
            table_name = "covid"
            table_header = ', '.join( ( column + " varchar" for column in csv_header ) )
            table_fields = ', '.join( ( "?" for column in range(0, len(csv_header)) ) )
            if table_primary_keys:
                table_pk = ", PRIMARY KEY (" + ', '.join( ( pk for pk in table_primary_keys ) ) + " )"
            
            create_table_query = "CREATE TABLE IF NOT EXISTS " + table_name + " ( " + table_header + " " + table_pk +  " );"
            insert_table_query = "INSERT INTO " + table_name + " VALUES ( " + table_fields + " );"
            
            if self.verbose:
                print("\nCreate table query:\n" + create_table_query)
                print("\nInsert data query:\n" + insert_table_query + "\n")
            
            conn = sqlite3.connect(sqlite_db_name)
            cur = conn.cursor()
            
            try:
                cur.execute(create_table_query)
                with open(csv_filename) as f:
                    reader = csv.reader(f)
                    for field in reader:
                        cur.execute(insert_table_query, field)
                if self.verbose:
                    print("File successfully uploaded into the database {}.".format(sqlite_db_name))
                return True
            except:
                print("Error while writing in the database: ' ", sys.exc_info()[1], " '")
                return False
            
            conn.commit()
            conn.close()
        else:
            print("Please provide a valid filename.")
            return False
                
            
    def get_csv_header(self, csv_filename: str) -> List[str]:
        """Gets the header from the CSV file.

        Args:
            csv_filename (str): File to get the header (first line) from.

        Returns:
            List[str]: Header in a list of strings.
        """        
        if self.verbose :
            print("\nGetting header from CSV file: '{}'...".format(csv_filename))
        try:
            with open(csv_filename) as f:
                reader = csv.reader(f)
                csv_header = next(reader)
                clean_header = [ column.replace('-', '_') for column in csv_header ]
                if self.verbose :
                    print("...got: '{}'.".format(clean_header))
                return clean_header
        except:
            print("Error while retrieving the CSV file's header. Check the file supplied.")
            return None
