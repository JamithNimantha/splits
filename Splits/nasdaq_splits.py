
__version__ = 1.1
__author__ = 'Jamith Nimantha'

import calendar
from datetime import datetime

from dateutil import relativedelta

import logger
import tools
from entry import Entry

log = logger.logger


class NasdaqSplits:
    def __init__(self, sql) -> None:
        self.base_link = "https://api.nasdaq.com/api/calendar/splits?date={}"
        self.sql = sql

    def __call__(self, ) -> None:
        today = datetime.today().date().strftime("%Y-%m-%d")
        self.get_month_data(today)

    def get_month_data(self, today: str) -> None:
        log.info(f"Today Date-> {today}")
        link = self.base_link.format(today)
        json_data = tools.parse_nasdaq_json(link)
        if not json_data:
            log.warning("failed to fetch the page")
            return
        success = 0
        for split_record in json_data['data']['rows']:
            try:
                announced_date = split_record['announcedDate']
                note = None
                if 'N/A' == split_record['announcedDate']:
                    announced_date = (datetime.today().date() - relativedelta.relativedelta(months=6)).strftime(
                        "%m/%d/%Y")
                    note = 'announcement_date invalid'
                entry = Entry(
                    sql=self.sql,
                    symbol=split_record['symbol'],
                    co_name=split_record['name'],
                    ratio=split_record['ratio'],
                    payable_date=split_record['payableDate'],
                    updated_timestamp=None,
                    exchange=None,
                    ann_date=announced_date,
                    rec_date=None,
                    ex_date=split_record['executionDate'],
                    optionable=None,
                    note=note,
                )
                if self.sql.insert_data(entry.sql_insert_data):
                    success += 1
            except Exception as e:
                log.error(e)
        else:
            log.info(f"{success} items saved to db")

