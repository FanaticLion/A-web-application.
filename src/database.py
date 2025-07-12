import psycopg2
from src.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def create_database():
    conn = psycopg2.connect(dbname='postgres', user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    cur.execute(f"CREATE DATABASE {DB_NAME}")
    cur.close()
    conn.close()


def create_tables():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE employers (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            hh_id TEXT UNIQUE
        );

        CREATE TABLE vacancies (
            id SERIAL PRIMARY KEY,
            employer_id INTEGER REFERENCES employers(id),
            title TEXT NOT NULL,
            salary INT,
            url TEXT
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()
