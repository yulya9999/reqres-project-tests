import requests
from utils.attach import response_attaching, response_logging


def request_sample(base_url, endpoint, method, data=None, params=None):
    url = f"{base_url}{endpoint}"
    response = requests.request(method, url, data=data, params=params)
    response_logging(response)
    response_attaching(response)
    return response
