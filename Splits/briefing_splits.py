__version__ = 1.1
__author__ = 'Jamith Nimantha'

from datetime import datetime
from typing import Optional

from dateutil import relativedelta
from dateutil import parser

import logger
import tools
from entry import Entry

log = logger.logger


class BriefingSplits:
    def __init__(self, sql) -> None:
        self.base_link = "https://www.briefing.com/Inv/content/Calendar/SplitsCalendar.htm"
        self.sql = sql

    def __call__(self, ) -> None:
        self.get_data()

    def get_data(self, ) -> None:
        soup = tools.prepare_soup(self.base_link)
        if not soup:
            log.warning("failed to fetch the page")
            return
        # table = soup.find_all('div', {'class': 'calRow'})
        # tbody = table.find('tbody')
        success = 0
        for row in soup.find_all('div', {'class': 'calRow'}):
            # if row.text.__contains__('No Splits for this month'):
            #     break
            try:
                symbol = row.find('span', {'class': 'ticker'}).text
                co_name = row.find('span', {'class': 'ticker'}).next_sibling.text.replace('Â', '').strip()
                ratio = row.find('span', {'class': 'calLABEL'}, text='Ratio: ').next_sibling.text.replace('-',
                                                                                                          ':').strip()
                payable_date = row.find('span', {'class': 'calLABEL'}, text='Payable: ').next_sibling.text.strip()
                ex_date = row.find('span', {'class': 'calLABEL'}, text='Ex-Date*: ').next_sibling.text.strip()
                announced_date = row.find('span', {'class': 'calLABEL'}, text='Announced: ').next_sibling.text.strip()
                optionable = row.find('span', {'class': 'calLABEL'}, text='Optionable: ').next_sibling.text.strip()
                optionable = self.get_optionable(optionable)
                entry = Entry(
                    sql=self.sql,
                    symbol=symbol,
                    co_name=co_name,
                    ratio=ratio,
                    payable_date=payable_date,
                    updated_timestamp=None,
                    exchange=None,
                    ann_date=announced_date,
                    rec_date=None,
                    ex_date=ex_date,
                    optionable=optionable,
                    note=None,
                )
                if self.sql.insert_data(entry.sql_insert_data):
                    success += 1
            except Exception as e:
                log.error(e)
        else:
            log.info(f"{success} items saved to db")

    @staticmethod
    def get_optionable(optionable: str) -> Optional[str]:
        if 'Yes' == optionable:
            return str(True)
        elif 'No' == optionable:
            return str(False)
        else:
            return None
