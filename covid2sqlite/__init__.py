from covid2sqlite import Covid2Sqlite

__version__ = '0.1.0'


if __name__ == "__main__":
    my_covid_data = Covid2Sqlite()
    filename = my_covid_data.get_csv_file()
    my_covid_data.save_csv_to_sqlite(csv_filename=filename)