import allure
import requests
import pytest
from data.data import TestData


# Проверка создания пользователя
class TestCreateUser:

    @allure.title('Пользователь создается успешно')
    def test_create_user_success(self, created_user):

        assert created_user is not None, "Созданный пользователь отсутствует"

        response = created_user["response"]
        assert response.status_code == 200, f"Ошибка при создании пользователя: {response.text}"

        data = response.json()
        assert data.get("success"), "Неуспешное создание пользователя"

    @pytest.mark.parametrize("payload, expected_status_code, expected_success, expected_message", [
        (
            {"email": TestData.EXISTING_EMAIL, "password": TestData.PASSWORD, "name": TestData.NAME},
            403,
            False,
            "User already exists"
        ),
    ])
    @allure.title('Нельзя создать двух одинаковых пользователей')
    def test_create_existing_user(self, created_user, payload, expected_status_code, expected_success, expected_message):

        response = requests.post(TestData.REGISTER_USER_API_URL, json={
            "email": created_user["email"],  # Используем email уже созданного пользователя
            "password": created_user["password"],
            "name": created_user["name"]
        })

        assert response.status_code == expected_status_code, f"Ошибка: {response.text}"
        data = response.json()
        assert data["success"] == expected_success, "Ожидалась ошибка, но запрос прошел успешно"
        assert data["message"] == expected_message, f"Ожидалось сообщение '{expected_message}', но получено '{data['message']}'"

    @pytest.mark.parametrize("payload", [
        {"email": TestData.EMAIL, "password": TestData.PASSWORD},  # Нет имени
        {"password": TestData.PASSWORD, "name": TestData.NAME},  # Нет email
        {"email": TestData.EMAIL, "name": TestData.NAME}  # Нет пароля
    ])
    @allure.title('Нельзя создать пользователя с незаполненным обязательным полем')
    def test_create_user_failed(self, payload):

        response = requests.post(TestData.REGISTER_USER_API_URL, json=payload)

        assert response.status_code == 403, f"Ошибка: {response.text}"
        data = response.json()
        assert data["success"] is False, "Запрос не должен быть успешным"
        assert data["message"] == TestData.TEXT_EMAIL_PASSWORD_AND_NAME_ARE_REQUIRED_FIELDS, "Неверное сообщение об ошибке"





