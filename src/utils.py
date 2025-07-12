def parse_salary(salary_data: dict) -> int:
    if salary_data and salary_data.get("from"):
        return salary_data["from"]
    return 0