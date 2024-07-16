import requests
from jsonschema import validate
from schemas.user import users_list, create_users, register_user, update_user_info


def test_all_the_users_should_have_unique_id(base_url):
    response = requests.get(url=f'{base_url}/users')
    body = response.json()
    ids = [element['id'] for element in body['data']]

    assert response.status_code == 200
    assert body['per_page'] == 6
    assert list(set(ids)) == ids
    validate(body, schema=users_list)


def test_get_user_id_does_not_exist(base_url):
    id_user = '23'
    response = requests.get(url=f'{base_url}/users/{id_user}')
    body = response.json()

    assert response.status_code == 404
    assert body == {}


def test_post_create_user(base_url):
    payload = {
        "name": "Yulia",
        "job": "tester"
    }
    response = requests.post(url=f'{base_url}/users', data=payload)
    body = response.json()

    assert response.status_code == 201
    assert body['name'] == "Yulia"
    assert body['job'] == "tester"
    validate(body, schema=create_users)


def test_post_register_user_successful(base_url):
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
    response = requests.post(url=f'{base_url}/register', data=payload)
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == 4

    validate(body, schema=register_user)


def test_post_register_user_unsuccessful(base_url):
    payload = {
        "email": "yul@reqres.in"
    }

    response = requests.post(url=f'{base_url}/register', data=payload)
    body = response.json()

    assert response.status_code == 400
    assert body['error'] == 'Missing password'


def test_put_update_user_info(base_url):
    payload = {
        "name": "Yulia",
        "job": "test engineer"
    }
    user_id = '2'

    response = requests.put(url=f'{base_url}/users/{user_id}', data=payload)
    body = response.json()

    assert response.status_code == 200
    assert body['job'] == "test engineer"
    validate(body, schema=update_user_info)


def test_delete_user_by_id(base_url):
    user_id = '2'
    response = requests.delete(url=f'{base_url}/users/{user_id}')

    assert response.status_code == 204
    assert response.text == ""
