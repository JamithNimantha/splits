import json
from typing import List, Union

import requests
from bs4 import BeautifulSoup

import logger

log = logger.logger


def read_json(filename: str) -> Union[List[dict], dict]:
    return json.load(open(filename, 'r', encoding='utf-8'))


def parse_json(link: str) -> Union[List[dict], dict]:
    response = requests.get(link, headers={"Accept": "application/json"})
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error : cannot fetch URL due to Status Code :{response.status_code}')


def prepare_soup(link: str) -> BeautifulSoup:
    html = requests.get(link)
    if html.status_code == 200:
        return BeautifulSoup(html.text, "html.parser")
    return None


if __name__ == "__main__":
    pass
