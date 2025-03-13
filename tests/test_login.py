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
        assert "accessToken" in data, "Отсутствует accessToken"
        assert "refreshToken" in data, "Отсутствует refreshToken"
        assert "user" in data, "Отсутствует информация о пользователе"
        assert data["user"]["email"] == authorized_user["email"], "Email пользователя не совпадает"
        assert data["user"]["name"] == authorized_user["name"], "Имя пользователя не совпадает"

    @pytest.mark.parametrize("payload", [
        {"email": "wrong_user@yndex.ru", "password": "696969"},  # Неверный email
        {"email": "ivan-ivanov6969@yandex.ru", "password": "p"},  # Неверный пароль
        {"email": "ivan-ivanov6969@yandex.ru"},  # Нет пароля
        {"password": "696969"}  # Нет email
    ])
    @allure.title("Ошибка авторизации с неверными данными")
    def test_login_failure(self, payload):

        response = requests.post(TestData.LOGIN_USER_API_URL, json=payload)

        assert response.status_code == 401, f"Ошибка: {response.text}"
        data = response.json()
        assert data["success"] is False, "Запрос не должен быть успешным"
        assert data["message"].strip().lower() == "email or password are incorrect", "Неверное сообщение об ошибке"
