import pytest
from src.headhunter_api import HeadHunterApi
from src.vacancy import Vacancy


@pytest.fixture
def api():
    return HeadHunterApi()


def test_get_vacancies_success():
    api = HeadHunterApi()
    vacancies = api.get_vacancies("Python", 1)
    assert isinstance(vacancies, list)
    assert all(isinstance(vac, Vacancy) for vac in vacancies)
    assert len(vacancies) > 0


def test_get_vacancies_error():
    api = HeadHunterApi()
    vacancies = api.get_vacancies("Несуществующее ключевое слово", 1)
    assert isinstance(vacancies, list)
    assert len(vacancies) == 0
