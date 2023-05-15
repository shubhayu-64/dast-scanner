import requests
# from app.helper import *


def test_api():
    url = 'http://localhost:5000/spider'
    payload = {'url': 'https://public-firing-range.appspot.com', 'ascan': False}
    response = requests.post(url, json=payload)

    assert response.status_code == 200
    # assert response.json()['status']
    print(response.json())


def test_parse():
    filename = 'app/scan_results.json'
    # parse_basic_result(filename)


def test_history():
    url = 'http://localhost:5000/history'
    payload = {'userId': 'local'}
    response = requests.post(url, json=payload)

    assert response.status_code == 200
    print(response.json())


def ping_server():
    url = 'http://localhost:5000/'
    response = requests.get(url)
    status = []
    for i in range(10):
        status.append(response.status_code)
    # assert response.status_code == 200
    print(status)


if __name__ == '__main__':
    ping_server()
    test_api()
    # test_history()
