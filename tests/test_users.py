import allure
from jsonschema import validate
from reqres_project_tests.schemas.user import users_list, create_users, update_user_info
from reqres_project_tests.utils.request_sample import request_sample


@allure.feature("Пользователь")
@allure.story("Проверка id пользователей на уникальность")
def test_all_the_users_should_have_unique_id(base_url):

    with allure.step("Отправка запроса"):
        response = request_sample(base_url, endpoint="/users", method="GET")
        body = response.json()
        ids = [element['id'] for element in body['data']]

    with allure.step("Проверка ответа"):
        assert response.status_code == 200
        assert body['per_page'] == 6
        assert list(set(ids)) == ids

    with allure.step("Проверка схемы"):
        validate(body, schema=users_list)


@allure.feature("Пользователь")
@allure.story("Получение  пользователя по несуществующему id")
def test_get_user_id_does_not_exist(base_url):
    id_user = '23'
    response = request_sample(base_url, endpoint=f"/users/{id_user}", method="GET")
    body = response.json()

    assert response.status_code == 404
    assert body == {}


@allure.feature("Пользователь")
@allure.story("Создание пользователя")
def test_post_create_user(base_url):
    payload = {
        "name": "Yulia",
        "job": "tester"
    }
    response = request_sample(base_url, endpoint="/users", method="POST", data=payload)
    body = response.json()

    assert response.status_code == 201
    assert body['name'] == "Yulia"
    assert body['job'] == "tester"
    validate(body, schema=create_users)


@allure.feature("Пользователь")
@allure.story("Обновление информации о пользователе")
def test_put_update_user_info(base_url):
    payload = {
        "name": "Yulia",
        "job": "test engineer"
    }
    user_id = '2'

    response = request_sample(base_url, endpoint=f"/users/{user_id}", method="PUT", data=payload)
    body = response.json()

    assert response.status_code == 200
    assert body['job'] == "test engineer"
    validate(body, schema=update_user_info)


@allure.feature("Пользователь")
@allure.story("Удаление пользователя по id")
def test_delete_user_by_id(base_url):
    user_id = '2'
    response = request_sample(base_url, endpoint=f"/users/{user_id}", method="DELETE")

    assert response.status_code == 204
    assert response.text == ""
