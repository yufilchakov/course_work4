import json
import os
from abc import ABC, abstractmethod

from config import DATA_PATH


class BaseWorker(ABC):
    """
    Абстрактный базовый класс для объектов, которые должны выполнять операции с вакансиями.
    Он содержит четыре абстрактных методов:
    """
    
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass
    
    @abstractmethod
    def add_vacancies(self, vacancies):
        pass
    
    @abstractmethod
    def del_vacancy(self, vacancy):
        pass
    
    @abstractmethod
    def select_vacancy(self, keyword):
        pass


class JSONWorker(BaseWorker):
    """
    Этот класс предоставляет основу для работы с данными в формате JSON, предполагая,
    что данные будут храниться в файле, имя которого указывается при создании экземпляра класса.
    """
    
    def __init__(self, file_name):
        self.file_path = os.path.join(DATA_PATH, file_name)
        self.prepare()
    
    def prepare(self):
        """
        Этот метод выполняет предварительную подготовку к работе с данными о вакансиях.
        """
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf 8') as file:
                json.dump([], file)
    
    def read_vacancies(self):
        """
        Метод для чтения всех вакансий из файла.
        Список словарей с данными о вакансиях.
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return [json.loads(line) for line in file]
    
    def write_vacancies(self, vacancies):
        """
        Метод для записи списка вакансий в файл.
        Список словарей с данными о вакансиях.
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(vacancies, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f'Ошибка записи файла: {e}')
    
    def add_vacancy(self, vacancy):
        """
        Метод для добавления одной вакансии.
        Словарь с данными о вакансии.
        """
        vacancies = self.read_vacancies()
        vacancies.append(vacancy)
        self.write_vacancies(vacancies)
    
    def add_vacancies(self, vacancies):
        """
        Метод для добавления нескольких вакансий.
        Список словарей с данными о вакансиях.
        """
        all_vacancies = self.read_vacancies()
        all_vacancies.extend(vacancies)
        self.write_vacancies(all_vacancies)
    
    def del_vacancy(self, vacancy_id):
        """
        Метод для удаления вакансии по её идентификатору.
        Идентификатор вакансии.
        """
        vacancies = self.read_vacancies()
        vacancies = [v for v in vacancies if v['id'] != vacancy_id]
        self.write_vacancies(vacancies)
    
    def select_vacancy(self, keyword):
        """
        Метод для выбора вакансий, содержащих указанное ключевое слово в заголовке.
        Ключевое слово для поиска в заголовках вакансий.
        Список словарей с данными о найденных вакансиях.
        """
        vacancies = self.read_vacancies()
        return [v for v in vacancies if keyword.lower() in v['title'].lower()]
