from configparser import ConfigParser

import pandas as pd
import psycopg2
from sqlalchemy import create_engine


def get_db_config(config_file="./config/database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(config_file)
    return dict(parser.items(section))


def create_database(db_params):
    """Create a PostgreSQL database."""
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            database="postgres",
            user=db_params["user"],
            password=db_params["password"],
            host=db_params["host"],
            port=db_params["port"],
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(f"DROP DATABASE IF EXISTS {db_params['database']}")
        cursor.execute(f"CREATE DATABASE {db_params['database']}")
        print(f"Database {db_params['database']} created successfully!")

    except Exception as e:
        print(f"Error creating database: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def execute_schema(db_params, schema_file):
    """Execute SQL schema file."""
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        with open(schema_file, "r") as file:
            schema_sql = file.read()
            cursor.execute(schema_sql)
            conn.commit()

        print("Schema created successfully!")

    except Exception as e:
        print(f"Error executing schema file: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def load_csv_data(db_url, csv_file, table_name):
    """Load CSV data into PostgreSQL table."""
    try:
        engine = create_engine(db_url)
        df = pd.read_csv(csv_file)
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"Table {table_name} created successfully!")

    except Exception as e:
        print(f"Error loading the data: {e}")
        raise


def main():
    CONFIG_FILE = "./config/database.ini"
    SCHEMA_FILE = "./scripts/sql/schema.sql"
    CSV_FILE = "./data/processed_game_logs.csv"

    db_params = get_db_config(config_file=CONFIG_FILE)

    create_database(db_params)
    execute_schema(db_params, SCHEMA_FILE)

    db_url = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
    load_csv_data(db_url, CSV_FILE, "game_logs")


if __name__ == "__main__":
    main()
