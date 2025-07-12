from src.db_manager import DBManager

def test_avg_salary():
    db = DBManager()
    avg = db.get_avg_salary()
    assert avg > 0