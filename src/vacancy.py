"""
Этот класс представляет собой модель для представления информации о вакансии.
Этот класс предоставляет удобный способ создания, хранения и представления информации о вакансиях,
а также позволяет сравнивать и сортировать вакансии на основе их зарплаты.
"""


class Vacancy:
    def __init__(self, title, url, salary, schedule, requirement, responsibility):
        self.title = title
        self.url = url
        self.salary = salary
        self.salary_to = salary
        self.salary_to = salary["from"] if salary["from"] is not None else 0
        self.salary_from = salary["to"] if salary["to"] is not None else 0
        self.schedule = schedule
        self.requirement = requirement if requirement else ""
        self.responsibility = responsibility if responsibility else ""
        
    def __lt__(self, other):
        return self.salary < other.salary
    
    def __gt__(self, other):
        return self.salary > other.salary
    
    @classmethod
    def from_dict(cls, vacancy_dict):
        salary = vacancy_dict.get('salary')
        return cls(
            title=vacancy_dict.get('name', ''),
            url=vacancy_dict.get('alternate_url', ''),
            salary=salary or {'from': 0, 'to': 0},
            schedule=vacancy_dict.get('schedule', {}).get('name', ''),
            requirement=vacancy_dict.get('snippet', {}).get('requirement', ''),
            responsibility=vacancy_dict.get('snippet', {}).get('responsibility', '')
        )
    
    def __str__(self):
        return (f'Название: {self.title}\n'
                f'Ссылка: {self.url}\n'
                f'Зарплата: {self.salary_to}-{self.salary_from}\n'
                f'График работы: {self.schedule}\n'
                f'Требования: {self.requirement}\n'
                f'Обязанности: {self.responsibility}\n')
