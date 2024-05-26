from abc import ABC, abstractmethod

import requests

from src.vacancy import Vacancy


class BaseAPI(ABC):
    """
    Класс предназначен для определения базового интерфейса API для получения вакансий.
    """
    
    @abstractmethod
    def get_vacancies(self, keyword, count):
        pass


class HeadHunterApi(BaseAPI):
    """
    Этот класс представляет конкретную реализацию интерфейса API для получения вакансий с сайта hh.ru.
    """
    
    def __init__(self):
        self.url = "https://api.hh.ru/vacancies/"
        self.params = {
            'text': '',
            'page': 0,
            'per_page': 100
        }
    
    def get_vacancies(self, keyword: str, count: int) -> list[Vacancy]:
        """
            Функция предназначена для получения вакансий с помощью запросов к API.
        """
        self.params.update({'text': keyword})
        self.params['per_page'] = count
        response = requests.get(self.url, params=self.params)
        if response.status_code == 200:
            vacancies_data = response.json().get('items', [])
            vacancies_data = vacancies_data[:count]
            vacancies = [Vacancy.from_dict(vacancy_data) for vacancy_data in vacancies_data]
            return vacancies
        print(f'Не удалось получить данные: {response.status_code}')
        return []
    