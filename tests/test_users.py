import requests
from jsonschema import validate
from schemas.user import *

url = 'https://reqres.in/api'


def test_all_the_users_should_have_unique_id():
    response = requests.get(url=f'{url}/users')
    body = response.json()
    ids = [element['id'] for element in body['data']]

    assert response.status_code == 200
    assert body['per_page'] == 6
    assert list(set(ids)) == ids
    validate(body, schema=users_list)


def test_get_user_id_does_not_exist():
    id_user = '23'
    response = requests.get(url=f'{url}/users/{id_user}')
    body = response.json()

    assert response.status_code == 404
    assert body == {}


def test_post_create_user():
    payload = {
        "name": "Yulia",
        "job": "tester"
    }
    response = requests.post(url=f'{url}/users', data=payload)
    body = response.json()

    assert response.status_code == 201
    assert body['name'] == "Yulia"
    assert body['job'] == "tester"
    validate(body, schema=create_users)
    return body['id']


def test_post_register_user_successful():
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
    response = requests.post(url=f'{url}/register', data=payload)
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == 4

    validate(body, schema=register_user)


def test_post_register_user_unsuccessful():
    payload = {
        "email": "yul@reqres.in"
    }

    response = requests.post(url=f'{url}/register', data=payload)
    body = response.json()

    assert response.status_code == 400
    assert body['error'] == 'Missing password'


def test_put_update_user_info():
    payload = {
        "name": "Yulia",
        "job": "test engineer"
    }

    response = requests.put(url=f'{url}/users/{test_post_create_user()}', data=payload)
    body = response.json()

    assert response.status_code == 200
    assert body['job'] == "test engineer"
    validate(body, schema=update_user_info)


def test_delete_user_by_id():
    response = requests.delete(url=f'{url}/users/{test_post_create_user()}')

    assert response.status_code == 204
    assert response.text == ""
