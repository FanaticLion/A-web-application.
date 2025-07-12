from src.api_hh import HHApi
from src.database import create_database, create_tables
from src.db_manager import DBManager
from src.utils import parse_salary

EMPLOYER_IDS = ["80", "1740", "3529", "78638", "93945", "4181", "39305", "1122462", "87021", "3776"]

if __name__ == "__main__":
    create_database()
    create_tables()

    api = HHApi(EMPLOYER_IDS)
    employers = api.get_employer_data()

    conn = DBManager()
    with conn.conn.cursor() as cur:
        for emp in employers:
            cur.execute("INSERT INTO employers (name, hh_id) VALUES (%s, %s) RETURNING id", (emp['name'], emp['id']))
            employer_id = cur.fetchone()[0]
            vacancies = api.get_vacancies(emp['id'])
            for vac in vacancies:
                salary = parse_salary(vac['salary'])
                cur.execute("""
                    INSERT INTO vacancies (employer_id, title, salary, url)
                    VALUES (%s, %s, %s, %s)
                """, (employer_id, vac['name'], salary, vac['alternate_url']))
        conn.conn.commit()

    print("--- Компании и кол-во вакансий ---")
    for row in conn.get_companies_and_vacancies_count():
        print(row)