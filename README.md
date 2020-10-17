# covid2sqlite

Quick tool to get COVID data and turn it into a sqlite database.
Useful for Web app (Django, etc.) models.

Import the package.
```python
from covid2sqlite import Covid2Sqlite
```

Create the object.
```python
# The parameter 'verbose' displays the filenames, URL, headers, etc.
my_covid_data = Covid2Sqlite(verbose=True)
```

Get the CSV file online.
```python
# If the parameter 'csv_file_url' is not provided, use the default URL: https://opendata.ecdc.europa.eu/covid19/casedistribution/csv
# The filename in return has this format 'covid_report_yyyy_mm_dd.csv' ( example : covid_report_2020_10_17.csv)
filename = my_covid_data.get_csv_file(csv_file_url="https://opendata.ecdc.europa.eu/covid19/casedistribution/csv")
```

Put the CSV file into the database. The script get automatically headers from csv and create corresponding headers in the database.
```python
# The default values are:
# sqlite_db_name: covid.db
# table_name: covid
# table_primary_keys: ["dateRep", "countriesAndTerritories", "geoId"]
# Therefore the only mandatory parameter is the filename if you use the default CSV file.
my_covid_data.save_csv_to_sqlite(csv_filename=filename, sqlite_db_name="covid.db", table_name="covid", table_primary_keys=["dateRep", "countriesAndTerritories", "geoId"])
```