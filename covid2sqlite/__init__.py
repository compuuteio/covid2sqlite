from covid2sqlite import Covid2Sqlite

__version__ = '0.1.0'


if __name__ == "__main__":
    mycovid = Covid2Sqlite()
    # print(mycovid.get_csv_file())
    mycovid.save_csv_to_sqlite("covid_report_2020_10_17.csv", table_primary_keys=["dateRep", "countriesAndTerritories", "geoId"])