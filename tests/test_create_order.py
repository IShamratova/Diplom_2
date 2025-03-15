import allure
import requests
from data.data import TestData


class TestCrateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, authorized_user, get_ingredients):
        headers = {"Authorization": authorized_user['accessToken']}
        payload = {"ingredients": get_ingredients[:2]}  # Берем два ингредиента из списка
        response = requests.post(TestData.ORDERS_API_URL, json=payload, headers=headers)

        assert response.status_code == 200, f"Ошибка при создании заказа: {response.text}"
        assert response.json()["success"] is True, "Система вернула неуспешный результат"
        assert "order" in response.json(), "Ответ не содержит данных о заказе"

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, get_ingredients):
        payload = {"ingredients": get_ingredients[:2]}
        response = requests.post(TestData.ORDERS_API_URL, json=payload)

        assert response.status_code == 200, f"Ошибка при создании заказа без авторизации: {response.text}"
        assert response.json()["success"] is True, "Система вернула неуспешный результат"
        assert "order" in response.json(), "Ответ не содержит данных о заказе"

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, authorized_user):
        headers = {"Authorization": authorized_user['accessToken']}
        payload = {"ingredients": []}  # Пустой список ингредиентов
        response = requests.post(TestData.ORDERS_API_URL, json=payload, headers=headers)

        assert response.status_code == 400, f"Ожидался 400, но получен {response.status_code}: {response.text}"
        assert response.json()["success"] is False, "Система вернула успешный результат, хотя ожидалась ошибка"
        assert response.json()["message"] == "Ingredient ids must be provided", "Неверное сообщение об ошибке"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredient(self, authorized_user):
        headers = {"Authorization": authorized_user['accessToken']}
        payload = {"ingredients": ["invalid_hash_123"]}  # Неверный хеш ингредиента
        response = requests.post(TestData.ORDERS_API_URL, json=payload, headers=headers)

        assert response.status_code == 500, f"Ожидался 500, но получен {response.status_code}: {response.text}"

