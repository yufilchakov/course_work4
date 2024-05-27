from abc import ABC, abstractmethod

import requests

from src.vacancy import Vacancy


class BaseAPI(ABC):
    """
    Класс предназначен для определения базового интерфейса API для получения вакансий.
    """
    
    @abstractmethod
    def get_vacancies(self, keyword):
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
    
    def get_vacancies(self, keyword: str) -> list[Vacancy]:
        """
            Функция предназначена для получения вакансий с помощью запросов к API.
        """
        self.params.update({'text': keyword})
        response = requests.get(self.url, params=self.params)
        if response.status_code == 200:
            return response.json().get('items', [])
        print(f'Не удалось получить данные: {response.status_code}')
        return []
    