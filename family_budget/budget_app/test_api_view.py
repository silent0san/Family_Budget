import pytest
from family_budget.budget_app.models import Budget, BudgetRecord
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


def test_get_budget(client):
    user_1 = User.objects.create_user('Chevy Chase', 'chevy@chase.com', 'chevyspassword')
    login = client.login(username='Chevy Chase', password='chevyspassword')

    budget_data = {
        "id": "7ce89192-15a1-4f99-b48d-8be0591d4bdd",
        "name": "Test_Name",
        "created_date": '2022-08-16T18:58:15.980702Z',
        "total_value": "0",
        "owner": user_1,
    }

    expected_data = {
        "id": "7ce89192-15a1-4f99-b48d-8be0591d4bdd",
        "name": "Test_Name",
        "created_date": '2022-08-16T18:58:15.980702Z',
        "total_value": "0.00",
        "owner": 1,
        "shared_with": []
    }

    budget = Budget(**budget_data)
    budget.save()

    response = client.get('/api/budget_list/')
    content = response.json()["results"][0]

    assert content == expected_data
    assert response.status_code == 200


def test_get_record(client):
    user_2 = User.objects.create_user('Chevy Chase', 'chevy@chase.com', 'chevyspassword')
    login = client.login(username='Chevy Chase', password='chevyspassword')

    budget_data = {
        "id": "7ce89192-15a1-4f99-b48d-8be0591d4bdd",
        "name": "Test_Name",
        "created_date": '2022-08-16T18:58:15.980702Z',
        "total_value": "0",
        "owner": user_2,
    }

    budget = Budget(**budget_data)
    budget.save()

    record_data = {
        "id": "1",
        "name": "Test_Name",
        "created_date": '2022-08-16T18:58:15.980702Z',
        "value": "-150",
        "budget": budget,
        "category": "Expanse"
    }

    expected_record_data = {
        "id": 1,
        "name": "Test_Name",
        "created_date": '2022-08-16T18:58:15.980702Z',
        "value": "-150.00",
        "budget": "7ce89192-15a1-4f99-b48d-8be0591d4bdd",
        "category": "Expanse"
    }

    record = BudgetRecord(**record_data)
    record.save()

    response = client.get('/api/api_record_management/7ce89192-15a1-4f99-b48d-8be0591d4bdd')
    content = response.json()["results"][0]

    assert content == expected_record_data
    assert response.status_code == 200
