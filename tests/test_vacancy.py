import pytest
from src.vacancy import Vacancy


@pytest.fixture()
def vacancy():
    return Vacancy


def test_vacancy_creation_with_valid_data():
    vacancy = Vacancy(
        title="Python Developer",
        url="https://api.hh.ru/vacancies/",
        salary={"from": 50000, "to": 70000},
        schedule="На постоянной основе",
        requirements="3+ года опыта",
        responsibility="Разрабатывать и поддерживать программное обеспечение"
    )
    assert vacancy.title == "Python Developer"
    assert vacancy.url == "https://api.hh.ru/vacancies/"
    assert isinstance(vacancy.salary, dict)
    assert vacancy.salary == {"from": 50000, "to": 70000}
    assert vacancy.schedule == "На постоянной основе"
    assert vacancy.requirements == "3+ года опыта"
    assert vacancy.responsibility == "Разрабатывать и поддерживать программное обеспечение"


def test_vacancy_creation_with_invalid_salary():
    vacancy = Vacancy(
        title="Python Developer",
        url="https://api.hh.ru/vacancies/",
        salary="invalid_salary",
        schedule="На постоянной основе",
        requirements="3+ года опыта",
        responsibility="Разрабатывать и поддерживать программное обеспечение"
    )
    assert vacancy.salary_from == 0
    assert vacancy.salary_to == 0
    assert "Предупреждение: неверные данные о зарплате, используются значения по умолчанию."


def test_vacancy_creation_with_negative_salary():
    vacancy = Vacancy(
        title="Python Developer",
        url="https://api.hh.ru/vacancies/",
        salary={"from": -50000, "to": 70000},
        schedule="На постоянной основе",
        requirements="3+ года опыта",
        responsibility="Разрабатывать и поддерживать программное обеспечение"
    )
    assert vacancy.salary_from == 0
    assert vacancy.salary_to != 70000
    assert "Предупреждение: обнаружены отрицательные значения зарплаты, установлены значения по умолчанию."


def test_vacancy_from_dict(vacancy):
    vacancy_dict = {
        "name": "Python Developer",
        "alternate_url": "https://api.hh.ru/vacancies/",
        "salary": {"from": 50000, "to": 70000},
        "schedule": {"name": "На постоянной основе"},
        "snippet": {"requirements": "3+ года опыта", "responsibility": "Разрабатывать и поддерживать программное обеспечение"}
    }
    vacancy = Vacancy.from_dict(vacancy_dict)
    assert vacancy.title == "Python Developer"
    assert vacancy.url == "https://api.hh.ru/vacancies/"
    assert vacancy.salary_from == 50000
    assert vacancy.salary_to == 70000
    assert vacancy.schedule == "На постоянной основе"
    assert vacancy.requirements == "3+ года опыта"
    assert vacancy.responsibility == "Разрабатывать и поддерживать программное обеспечение"
