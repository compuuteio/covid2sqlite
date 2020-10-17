import csv

import sqlite3
from datetime import datetime
from typing import List, Optional

import requests
import sys

class Covid2Sqlite():
    
    csv_source_url: str = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        
    def get_csv_file(self, csv_file_url: Optional[str]=None) -> str:
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
                print("\n" + create_table_query)
                print("\n" + insert_table_query + "\n")
            
            conn = sqlite3.connect(sqlite_db_name)
            cur = conn.cursor()
            
            try:
                cur.execute(create_table_query)
                with open(csv_filename) as f:
                    reader = csv.reader(f)
                    for field in reader:
                        cur.execute(insert_table_query, field)
            except:
                print("Error while writing in the database: ' ", sys.exc_info()[1], " '")
            
            conn.commit()
            conn.close()
            
    def get_csv_header(self, csv_filename: str) -> List[str]:
        if self.verbose :
            print("Getting header from CSV file: '{}'...".format(csv_filename))
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
