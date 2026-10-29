import getpass
import psycopg

password = getpass.getpass("PostgreSQL password: ")

with psycopg.connect(
    host="localhost", port=5432, user="postgres",
    password=password, dbname="postgres", autocommit=True,
) as conn:
    conn.execute("CREATE DATABASE library")
    print("Database 'library' created.")