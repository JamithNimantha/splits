__version__ = 1.1
__author__ = 'Jamith Nimantha'

from datetime import datetime

from dateutil import relativedelta

import logger
import tools
from entry import Entry

log = logger.logger


class FidelitySplits:
    def __init__(self, sql) -> None:
        self.base_link = "https://eresearch.fidelity.com/eresearch/conferenceCalls.jhtml?tab=splits&begindate={}"
        self.sql = sql

    def __call__(self, ) -> None:
        today = datetime.today().date()
        today = today.replace(day=1)
        if __import__('sys').platform.startswith('win'):
            prev_month = (today - relativedelta.relativedelta(months=1)).strftime("%#m/%#d/%Y")
            curr_month = today.strftime("%#m/%#d/%Y")
            next_month = (today + relativedelta.relativedelta(months=1)).strftime("%#m/%#d/%Y")
            next_month_2 = (today + relativedelta.relativedelta(months=2)).strftime("%#m/%#d/%Y")
        else:
            prev_month = (today - relativedelta.relativedelta(months=1)).strftime("%-m/%-d/%Y")
            curr_month = today.strftime("%-m/%-d/%Y")
            next_month = (today + relativedelta.relativedelta(months=1)).strftime("%-m/%-d/%Y")
            next_month_2 = (today + relativedelta.relativedelta(months=2)).strftime("%-m/%-d/%Y")

        for month in [prev_month, curr_month, next_month, next_month_2]:
            self.get_month_data(month)

    def get_month_data(self, month: str) -> None:
        log.info(f"Month -> {month}")
        link = self.base_link.format(month)
        soup = tools.prepare_soup(link)
        if not soup:
            log.warning("failed to fetch the page")
            return
        try:
            table = soup.find('table', {'class': 'datatable-component events-calender-table-four'})
            tbody = table.find('tbody')
            success = 0
            for tr in tbody.find_all('tr'):
                if tr.text.__contains__('No Splits for this month'):
                    break
                try:
                    co_name = tr.find('th').find('a').text
                    tds = tr.find_all('td')
                    symbol = tds[0].text.strip()
                    ratio = tds[1].text.strip()
                    ann_date = tds[2].text.strip()
                    rec_date = tds[3].text.strip()
                    ex_date = tds[4].text.strip()
                    entry = Entry(
                        sql=self.sql,
                        symbol=symbol,
                        co_name=co_name,
                        ratio=ratio,
                        payable_date=None,
                        updated_timestamp=None,
                        exchange=None,
                        ann_date=ann_date,
                        rec_date=rec_date,
                        ex_date=ex_date,
                        optionable=None,
                        note=None,
                    )
                    if self.sql.insert_data(entry.sql_insert_data):
                        success += 1
                except Exception as e:
                     log.error(e)
        except Exception as e:
            log.error(e)
        else:
            log.info(f"{success} items saved to db")

