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


def parse_nasdaq_json(link: str) -> Union[List[dict], dict]:
    headers = {
        'authority': 'api.nasdaq.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/93.0.4577.82 Safari/537.36',
        'origin': 'https://www.nasdaq.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.nasdaq.com/',
        'accept-language': 'en-US,en;q=0.9,si;q=0.8',
    }
    response = requests.get(link, headers=headers)
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
