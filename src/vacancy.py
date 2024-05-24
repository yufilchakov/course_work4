"""
Этот класс представляет собой модель для представления информации о вакансии.
Этот класс предоставляет удобный способ создания, хранения и представления информации о вакансиях,
а также позволяет сравнивать и сортировать вакансии на основе их зарплаты.
"""


class Vacancy:
    def __init__(self, title, url, salary, schedule, requirements, responsibility):
        self.title = title
        self.url = url
        self.salary = salary
        self.schedule = schedule
        self.requirements = requirements if requirements else ""
        self.responsibility = responsibility if responsibility else ""
        self.validate()
        
    def validate(self):
        if not isinstance(self.salary, dict) or 'from' not in self.salary or 'to' not in self.salary:
            self.salary = {'from': 0, 'to': 0}
            print("Предупреждение: неверные данные о зарплате, используются значения по умолчанию.")
            self.salary_from = 0
            self.salary_to = 0
            return
        
        self.salary_from = self.salary['from'] if self.salary['from'] is not None else 0
        self.salary_to = self.salary['to'] if self.salary['to'] is not None else 0
        
        if self.salary_from < 0 or self.salary_to < 0:
            self.salary_from = 0
            self.salary_to = 0
            print("Предупреждение: обнаружены отрицательные значения зарплаты, "
                  "установлены значения по умолчанию.")
        
    def __lt__(self, other):
        return self.salary < other.salary
        
    @classmethod
    def from_dict(cls, vacancy_dict):
        return cls(
            title=vacancy_dict.get('name'),
            url=vacancy_dict.get('alternate_url'),
            salary=vacancy_dict.get('salary', {}),
            schedule=vacancy_dict.get('schedule', {}).get('name', ''),
            requirements=vacancy_dict.get('snippet', {}).get('requirements', ''),
            responsibility=vacancy_dict.get('snippet', {}).get('responsibility', '')
        )
    
    def __str__(self):
        return (f'Название: {self.title}\n'
                f'Ссылка: {self.url}\n'
                f'Зарплата: {self.salary_from}-{self.salary_to}\n'
                f'График работы: {self.schedule}\n'
                f'Требования: {self.requirements}\n'
                f'Обязанности: {self.responsibility}\n')
    