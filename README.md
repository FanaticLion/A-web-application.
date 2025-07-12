##Структура проекта 
hh_vacancies_analysis/
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
│
├── src/
│   ├── __init__.py
│   ├── api_hh.py
│   ├── config.py
│   ├── database.py
│   ├── db_manager.py
│   ├── utils.py
│   └── tests/
│       ├── __init__.py
│       └── test_db_manager.py
│
└── data/ (optional)
.env файл
  DB_NAME=hh_vacancies
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432 
gitignore
 .env
__pycache__/
*.pyc
*.pyo
*.pyd
.DS_Store
venv/ 
 # Анализ вакансий с HeadHunter

Проект для сбора и анализа вакансий с API HeadHunter.

## Установка

1. Клонировать репозиторий:
```bash
git clone https://github.com/ваш-репозиторий/hh_vacancies_analysis.git
cd hh_vacancies_analysis
pip install -r requirements.txt
python main.py 
Функционал
Получение данных о компаниях с HH API

Сбор вакансий по компаниям

Сохранение в базу данных PostgreSQL

Аналитические запросы:

Количество вакансий по компаниям

Средняя зарплата

Вакансии с зарплатой выше средней

Поиск по ключевым словам

Структура проекта
src/api_hh.py - работа с API HeadHunter

src/database.py - создание БД и таблиц

src/db_manager.py - управление данными в БД

src/utils.py - вспомогательные функции

src/tests/ - тесты
Требования
Python 3.8+

PostgreSQL

Библиотеки из requirements.txt
requests==2.28.1
psycopg2-binary==2.9.3
python-dotenv==0.21.0
pytest==7.2.0
main.py
```python
from src.api_hh import HHApi
from src.database import create_database, create_tables
from src.db_manager import DBManager
from src.utils import parse_salary

EMPLOYER_IDS = ["80", "1740", "3529", "78638", "93945", 
               "4181", "39305", "1122462", "87021", "3776"]

def main():
    # Инициализация БД
    create_database()
    create_tables()
    
    # Получение данных с HH
    api = HHApi(EMPLOYER_IDS)
    employers = api.get_employer_data()
    
    # Сохранение в БД
    db = DBManager()
    with db.conn.cursor() as cur:
        for emp in employers:
            cur.execute(
                "INSERT INTO employers (name, hh_id) VALUES (%s, %s) RETURNING id", 
                (emp['name'], emp['id'])
            )
            employer_id = cur.fetchone()[0]
            
            vacancies = api.get_vacancies(emp['id'])
            for vac in vacancies:
                salary = parse_salary(vac.get('salary'))
                cur.execute(
                    """INSERT INTO vacancies (employer_id, title, salary, url)
                    VALUES (%s, %s, %s, %s)""",
                    (employer_id, vac['name'], salary, vac['alternate_url'])
                )
        db.conn.commit()
    
    # Вывод результатов
    print("--- Компании и количество вакансий ---")
    for row in db.get_companies_and_vacancies_count():
        print(f"{row[0]}: {row[1]} вакансий")

if __name__ == "__main__":
    main()
tests/test_db_manager.py
import pytest
from src.db_manager import DBManager
from src.database import create_database, create_tables

@pytest.fixture
def db_manager():
    create_database()
    create_tables()
    return DBManager()

def test_get_companies_and_vacancies_count(db_manager):
    result = db_manager.get_companies_and_vacancies_count()
    assert isinstance(result, list)

def test_get_avg_salary(db_manager):
    avg = db_manager.get_avg_salary()
    assert avg >= 0

def test_get_vacancies_with_keyword(db_manager):
    result = db_manager.get_vacancies_with_keyword("python")
    assert isinstance(result, list)
Для запуска тестов:
pytest src/tests/