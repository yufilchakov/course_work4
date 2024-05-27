from typing import List

from src.headhunter_api import HeadHunterApi
from src.vacancy import Vacancy
from src.worker import JSONWorker


def filter_vacancies(vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    """
    Фильтрует список вакансий по заданным ключевым словам.
    """
    return [v for v in vacancies if all(k in v.requirement for k in keywords)]


def sort_vacancies(vacancies, salary_from, salary_to):
    """
    Функция сортирует список вакансий по убыванию зарплаты.
    """
    return sorted(vacancies, key=lambda v: (v.salary_to if v.salary_to < salary_to and v.salary_from > salary_from
                                            else 0), reverse=True)


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

    hh_vacancies = hh_api.get_vacancies(search_query)
    vacancies = [Vacancy.from_dict(vacancy_dict) for vacancy_dict in hh_vacancies]
    file_worker = JSONWorker('vacancies.json')
    file_worker.write_vacancies(hh_vacancies)

    filtered_vacancies = filter_vacancies(vacancies, filter_words)
    sorted_vacancies = sort_vacancies(filtered_vacancies, salary_from, salary_to)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)
    
    