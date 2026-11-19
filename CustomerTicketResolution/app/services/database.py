
import sqlite3
import csv
import os

DB_PATH = "data/support.db"


def get_connection():

    return sqlite3.connect(DB_PATH)


def import_csv(table_name, filename):

    connection = get_connection()
    cursor = connection.cursor()

    filepath = f"data/{filename}"

    with open(filepath, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        columns = reader.fieldnames

        column_definition = ", ".join(
            f"{column} TEXT"
            for column in columns
        )

        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} "
            f"({column_definition})"
        )

        cursor.execute(f"DELETE FROM {table_name}")

        placeholders = ", ".join(
            ["?"] * len(columns)
        )

        query = (
            f"INSERT INTO {table_name} "
            f"VALUES ({placeholders})"
        )

        rows = [
            tuple(row[column] for column in columns)
            for row in reader
        ]

        cursor.executemany(query, rows)

    connection.commit()
    connection.close()

    print(f"Imported {len(rows)} records into {table_name}")


def initialize_database():

    import_csv("customers", "customers.csv")
    import_csv("hotels", "hotels.csv")
    import_csv("bookings", "bookings.csv")
    import_csv("tickets", "tickets.csv")
    import_csv("resolutions", "resolutions.csv")


if __name__ == "__main__":
    initialize_database()
