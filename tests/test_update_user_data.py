import allure
import requests
import pytest
from faker import Faker
from data.data import TestData

fake = Faker()


class TestUpdateUserData:

    @allure.title("Изменение данных авторизованного пользователя")
    @pytest.mark.parametrize("update_payload", [
        {"email": f"{fake.random_int()}_newemail@yandex.ru", "expected_key": "email"},  # Генерация уникального email
        {"name": "New Name", "expected_key": "name"}
    ])
    def test_update_user_authorized(self, authorized_user, update_payload):
        response = requests.get(TestData.USER_API_URL, headers={"Authorization": authorized_user["accessToken"]})

        assert response.status_code == 200, f"Ошибка: {response.text}"
        data = response.json()
        assert data["success"] is True, "Запрос неуспешен"

        headers = {"Authorization": authorized_user["accessToken"]}
        response = requests.patch(TestData.USER_API_URL, json=update_payload, headers=headers)

        assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code}: {response.text}"
        data = response.json()
        assert data["success"] is True, "Запрос неуспешен"

        response = requests.get(TestData.USER_API_URL, headers={"Authorization": authorized_user["accessToken"]})

        assert response.status_code == 200, f"Ошибка: {response.text}"
        data = response.json()
        assert data["success"] is True, "Запрос неуспешен"
        assert data["user"].get(update_payload.get("expected_key")) != authorized_user.get(update_payload.get("expected_key")), "Поле не обновлено"

    @pytest.mark.parametrize("update_payload", [
        {"email": "unauthemail@yandex.ru"},
        {"name": "Unauthorized Name"},
        {"password": "unauthpassword69"}
    ])
    @allure.title("Попытка изменить данные без авторизации с ожиданием ошибки")
    def test_update_user_unauthorized(self, update_payload):

        response = requests.patch(TestData.USER_API_URL, json=update_payload)

        assert response.status_code == 401, f"Ожидался 401, но получен {response.status_code}: {response.text}"
        data = response.json()
        assert data["success"] is False, "Запрос не должен быть успешным"
        assert data["message"] == TestData.TEXT_YOU_SHOULD_BE_AUTHORIZED, "Неверное сообщение об ошибке"

    @pytest.mark.parametrize("update_payload", [
        {"email": "existing_user@yandex.ru"}  # Уже существующий email
    ])
    @allure.title("Попытка обновить email на уже существующий")
    def test_update_user_existing_email(self, authorized_user, update_payload):

        headers = {"Authorization": authorized_user["accessToken"]}
        response = requests.patch(TestData.USER_API_URL, json=update_payload, headers=headers)

        assert response.status_code == 403, f"Ожидался 403, но получен {response.status_code}: {response.text}"
        data = response.json()
        assert data["success"] is False, "Запрос не должен быть успешным"
        assert data["message"] == TestData.TEXT_USER_WITH_SUCH_EMAIL_ALREADY_EXISTS, "Неверное сообщение об ошибке"




