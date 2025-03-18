import allure
import requests
import pytest
from data.data import TestData


class TestLoginUser:

    @allure.title("Успешная авторизация пользователя")
    def test_login_success(self, authorized_user):

        response = requests.post(TestData.LOGIN_USER_API_URL, json={
            "email": authorized_user["email"],
            "password": authorized_user["password"]
        })

        assert response.status_code == 200, f"Ошибка: {response.text}"
        data = response.json()
        assert data["success"] is True, "Запрос неуспешен"

    @pytest.mark.parametrize("payload", [
        {"email": TestData.WRONG_EMAIL, "password": TestData.PASSWORD},  # Неверный email
        {"email": TestData.EMAIL, "password": TestData.WRONG_PASSWORD},  # Неверный пароль
        {"email": TestData.EMAIL},  # Нет пароля
        {"password": TestData.PASSWORD}  # Нет email
    ])
    @allure.title("Ошибка авторизации с неверными данными")
    def test_login_failure(self, payload):

        response = requests.post(TestData.LOGIN_USER_API_URL, json=payload)

        assert response.status_code == 401, f"Ошибка: {response.text}"
        data = response.json()
        assert data["success"] is False, "Запрос не должен быть успешным"
        assert data["message"].strip().lower() == TestData.TEXT_EMAIL_OR_PASSWORD_ARE_INCORRECT, "Неверное сообщение об ошибке"
