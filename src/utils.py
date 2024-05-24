from src.headhunter_api import HeadHunterApi
from src.vacancy import Vacancy
from src.worker import JSONWorker


def filter_vacancies(get_vacancies, keywords):
    vacancies = [Vacancy.from_dict(v) for v in get_vacancies if isinstance(v, dict)]
    return [v for v in vacancies if all(k in v.requirements for k in keywords)]
    
    
def salary_range(self, salary_from, salary_to):
    if salary_from is None or salary_to is None:
        raise ValueError('Должны быть указаны значения «зарплата_от» и «зарплата_до»')
    vacancies = self.read_vacancies()
    return [v for v in vacancies if salary_from <= v['salary']['from'] <= salary_to]
    

def sort_vacancies(get_vacancies):
    return sorted(get_vacancies, key=lambda v: v.salary_range, reverse=True)


def get_top_vacancies(get_vacancies, n):
    return get_vacancies[:n]


def print_vacancies(get_vacancies):
    for vacancy in get_vacancies:
        print(vacancy)


def user_interaction():
    hh_api = HeadHunterApi()
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")
    
    hh_vacancies = hh_api.get_vacancies(search_query,5)
    vacancies_list = hh_vacancies
    
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    sorted_vacancies = sort_vacancies(filtered_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)
    
    file_worker = JSONWorker('vacancies.json')
    file_worker.read_vacancies()
    
    for vacancy in hh_vacancies:
        print(vacancy)
