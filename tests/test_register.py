import allure
from jsonschema import validate

from reqres_project_tests.schemas.user import register_user
from reqres_project_tests.utils.request_sample import request_sample


@allure.feature("Регистрация")
class TestRegister:

    @allure.story("Регистрация с валидными данными")
    def test_post_register_user_successful(self, base_url):
        payload = {
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
        response = request_sample(base_url, endpoint="/register", method="POST", data=payload)
        body = response.json()

        assert response.status_code == 200
        assert body["id"] == 4

        validate(body, schema=register_user)

    @allure.story("Регистрация с невалидными данными (отсутствует пароль)")
    def test_post_register_user_unsuccessful(self, base_url):
        payload = {
            "email": "yul@reqres.in"
        }

        response = request_sample(base_url, endpoint="/register", method="POST", data=payload)
        body = response.json()

        assert response.status_code == 400
        assert body['error'] == 'Missing password'
