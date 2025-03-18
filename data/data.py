class TestData:
    # URL тестового стенда
    BASE_API_URL = "https://stellarburgers.nomoreparties.site/api/"
    REGISTER_USER_API_URL = BASE_API_URL + "auth/register"
    LOGIN_USER_API_URL = BASE_API_URL + "auth/login"
    USER_API_URL = BASE_API_URL + "auth/user"
    ORDERS_API_URL = BASE_API_URL + "orders"
    INGREDIENTS_API_URL = BASE_API_URL + "ingredients"

    EMAIL = "ivan-ivanov6969@yandex.ru"
    EXISTING_EMAIL = "existing_user@yandex.ru"
    WRONG_EMAIL = "wrong_user@yndex.ru"
    PASSWORD = "696969"
    WRONG_PASSWORD = "p"
    NAME = "Ivan"

    TEXT_YOU_SHOULD_BE_AUTHORIZED = "You should be authorised"
    TEXT_EMAIL_PASSWORD_AND_NAME_ARE_REQUIRED_FIELDS = "Email, password and name are required fields"
    TEXT_EMAIL_OR_PASSWORD_ARE_INCORRECT = "email or password are incorrect"
    TEXT_USER_WITH_SUCH_EMAIL_ALREADY_EXISTS = "User with such email already exists"
    TEXT_INGREDIENT_IDS_MUST_BE_PROVIDED = "Ingredient ids must be provided"







