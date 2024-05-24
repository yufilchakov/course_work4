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
            data = response.json()
            vacancies = []
            for item in data['items']:
                salary = item.get('salary')
                salary_from = salary['from'] if salary and 'from' in salary else 0
                salary_to = salary['to'] if salary and 'to' in salary else 0
                vacancies.append(
                    Vacancy(
                        title=item.get('name'),
                        url=item.get('alternate_url'),
                        salary={'from': salary_from, 'to': salary_to},
                        schedule=item.get('schedule', {}).get('name', ''),
                        requirements=item.get('snippet', {}).get('requirements', ''),
                        responsibility=item.get('snippet', {}).get('responsibility', '')
                        )
                    )
            return vacancies
        else:
            print(f'Не удалось получить данные.: {response.status_code}')
        return []
 