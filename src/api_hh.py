import requests
from typing import List, Dict

BASE_URL = "https://api.hh.ru/employers"

class HHApi:
    def __init__(self, employers: List[str]):
        self.employers = employers

    def get_employer_data(self) -> List[Dict]:
        data = []
        for employer_id in self.employers:
            response = requests.get(f"{BASE_URL}/{employer_id}")
            if response.status_code == 200:
                data.append(response.json())
        return data

    def get_vacancies(self, employer_id: str) -> List[Dict]:
        url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
        response = requests.get(url)
        return response.json().get("items", [])