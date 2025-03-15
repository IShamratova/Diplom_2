import allure
import requests
from data.data import TestData


class TestGetUserOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth(self, authorized_user, get_ingredients):
        headers = {"Authorization": authorized_user['accessToken']}
        payload = {"ingredients": get_ingredients[:2]}  # Берем два ингредиента из списка
        response = requests.post(TestData.ORDERS_API_URL, json=payload, headers=headers)

        assert response.status_code == 200, f"Ошибка при создании заказа: {response.text}"
        assert response.json()["success"] is True, "Система вернула неуспешный результат"
        assert "order" in response.json(), "Ответ не содержит данных о заказе"

        headers = {"Authorization": authorized_user["accessToken"]}
        response = requests.get(TestData.ORDERS_API_URL, headers=headers)

        assert response.status_code == 200, f"Ошибка: {response.text}"
        data = response.json()
        assert data["success"] is True, "Запрос неуспешен"
        assert "orders" in data, "Ответ не содержит список заказов"
        assert isinstance(data["orders"], list), "Заказы должны быть списком"

    @allure.title("Получение заказов без авторизации")
    def test_get_orders_without_auth(self):
        response = requests.get(TestData.ORDERS_API_URL)

        assert response.status_code == 401, f"Ошибка: {response.text}"
        data = response.json()
        assert data["success"] is False, "Запрос должен быть неуспешным"
        assert data["message"] == "You should be authorised", "Неверное сообщение об ошибке"
