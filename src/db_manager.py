import psycopg2
from typing import List
from src.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    def get_companies_and_vacancies_count(self) -> List:
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, COUNT(v.id)
                FROM employers e
                LEFT JOIN vacancies v ON e.id = v.employer_id
                GROUP BY e.name
            """)
            return cur.fetchall()

    def get_all_vacancies(self) -> List:
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
            """)
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        with self.conn.cursor() as cur:
            cur.execute("SELECT AVG(salary) FROM vacancies")
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List:
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT title, salary
                FROM vacancies
                WHERE salary > (SELECT AVG(salary) FROM vacancies)
            """)
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List:
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT title, url FROM vacancies
                WHERE title ILIKE %s
            """, (f'%{keyword}%',))
            return cur.fetchall()
