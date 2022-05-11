
__author__ = "Jamith Nimantha"
__version__ = 1.0

import calendar
from datetime import datetime

from dateutil import relativedelta

import logger
import tools
from entry import Entry

log = logger.logger


class BenzingaSplits:
    def __init__(self, sql) -> None:
        self.base_link = "https://api.benzinga.com/api/v2.1/calendar/splits?token=1c2735820e984715bc4081264135cb90" \
                         "&parameters[date_from]={}&parameters[date_to]={}&parameters[" \
                         "date_sort]=ex&pagesize=1000"
        self.sql = sql

    def __call__(self, ) -> None:
        today = datetime.today().date()
        today = today.replace(day=1)
        date_from = (today - relativedelta.relativedelta(months=6)).strftime("%Y-%m-%d")
        # calendar.monthrange() used to get the last day of the month
        today = today.replace(day=calendar.monthrange(today.year, today.month)[1])
        date_to = (today + relativedelta.relativedelta(months=6)).strftime("%Y-%m-%d")

        self.get_month_data(date_from, date_to)

    def get_month_data(self, date_from: str, date_to: str) -> None:
        log.info(f"Date From -> {date_from} : Date To -> {date_to}")
        link = self.base_link.format(date_from, date_to)
        json_data = tools.parse_json(link)
        if not json_data:
            log.warning("failed to fetch the page")
            return
        success = 0
        for split_record in json_data['splits']:
            try:
                entry = Entry(
                    sql=self.sql,
                    symbol=split_record['ticker'],
                    co_name=split_record['name'],
                    ratio=split_record['ratio'],
                    payable_date=split_record['date_distribution'],
                    updated_timestamp=datetime.fromtimestamp(split_record['updated']).strftime("%m/%d/%Y"),
                    exchange=split_record['exchange'],
                    ann_date=split_record['date_announced'],
                    rec_date=split_record['date_recorded'],
                    ex_date=split_record['date_ex'],
                    optionable=split_record['optionable'],
                    note=split_record['notes'],
                )
                if self.sql.insert_data(entry.sql_insert_data):
                    success += 1
            except Exception as e:
                log.error(e)
        else:
            log.info(f"{success} items saved to db")

