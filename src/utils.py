from typing import List

from src.headhunter_api import HeadHunterApi
from src.vacancy import Vacancy
from src.worker import JSONWorker


def filter_vacancies(vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    """
    Фильтрует список вакансий по заданным ключевым словам.
    """
    return [v for v in vacancies if all(k in v.requirements for k in keywords)]


def salary_range(vacancies, salary_from, salary_to):
    """
    Функция для фильтрации списка вакансий по зарплатному диапазону.
    """
    if not (isinstance(salary_from, int) and isinstance(salary_to, int)):
        raise ValueError('Значения зарплат должны быть целыми числами')
    if salary_from == 0 and salary_to == 0:
        filtered_vacancies = [v for v in vacancies if v.salary.from_ == 0 and v.salary.to == 0]
    else:
        filtered_vacancies = [
            v for v in vacancies
            if v.salary.from_ >= salary_from and v.salary.to <= salary_to
        ]
    return filtered_vacancies


def sort_vacancies(vacancies, salary_from, salary_to):
    """
    Функция сортирует список вакансий по убыванию зарплаты.
    """
    return sorted(vacancies, key=lambda v: (v.salary.to if salary_from <= v.salary.from_ <= salary_to else 0), reverse=True)


def get_top_vacancies(get_vacancies, n):
    """
    Функция для получения первых n элементов из списка вакансий.
    """
    return get_vacancies[:n]


def print_vacancies(get_vacancies):
    """
    Функция для вывода информации о каждой вакансии из списка
    """
    for vacancy in get_vacancies:
        print(vacancy)


def user_interaction():
    hh_api = HeadHunterApi()
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_from, salary_to = map(int, input("Введите диапазон зарплат: ").split('-'))
    
    hh_vacancies = hh_api.get_vacancies(search_query, top_n)
    vacancies_list = hh_vacancies
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    sorted_vacancies = sort_vacancies(filtered_vacancies, salary_from, salary_to)
    top_vacancies = get_top_vacancies(sorted_vacancies,top_n)
    print_vacancies(top_vacancies)
    
    file_worker = JSONWorker('vacancies.json')
    file_worker.read_vacancies()
    
    for vacancy in hh_vacancies:
        print(vacancy)
