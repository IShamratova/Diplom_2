import pytest
import requests
from faker import Faker
from data.data import TestData

fake = Faker()


@pytest.fixture
def created_user():
    #Создаёт нового пользователя без авторизации и возвращает его данные.
    email = f"{fake.random_int()}_{fake.email()}" # Генерируем уникальный email
    password = fake.password()
    name = fake.name()

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(TestData.REGISTER_USER_API_URL, json=payload)
    assert response.status_code == 200, f"Ошибка при создании пользователя: {response.text}"

    data = response.json()
    assert data["success"] is True, "Неуспешное создание пользователя"

    return {
        "email": email,
        "password": password,
        "name": name
    }


@pytest.fixture
def logged_in_user(created_user):
    # Авторизует уже созданного пользователя и возвращает данные с токенами.
    payload = {
        "email": created_user["email"],
        "password": created_user["password"]
    }

    response = requests.post(TestData.LOGIN_USER_API_URL, json=payload)
    assert response.status_code == 200, f"Ошибка при авторизации: {response.text}"

    data = response.json()
    assert data["success"] is True, "Неуспешный вход"

    return {
        "email": created_user["email"],
        "password": created_user["password"],
        "name": created_user["name"],
        "accessToken": data["accessToken"],
        "refreshToken": data["refreshToken"]
    }


@pytest.fixture
def get_ingredients():
    # Получает список доступных ингредиентов
    response = requests.get(TestData.INGREDIENTS_API_URL)
    assert response.status_code == 200, f"Ошибка при получении ингредиентов: {response.text}"

    data = response.json()
    assert data["success"] is True, "Неуспешный запрос ингредиентов"
    assert "data" in data, "Ответ не содержит списка ингредиентов"

    return [ingredient["_id"] for ingredient in data["data"]]


@pytest.fixture
def authorized_user(logged_in_user):
    # Авторизует пользователя и удаляет его после теста.
    yield logged_in_user

    # Удаляем пользователя после теста
    headers = {"Authorization": logged_in_user["accessToken"]}
    response = requests.delete(TestData.USER_API_URL, headers=headers)
    data = response.json()
    assert data["message"] == "User successfully removed", "Пользователь не удалён"

    headers = {"Authorization": logged_in_user["accessToken"]}
    response = requests.get(TestData.ORDERS_API_URL, headers=headers)

    assert response.status_code == 200, f"Ошибка: {response.text}"