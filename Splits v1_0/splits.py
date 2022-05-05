__version__ = 1.0
__auther__ = "Shishere"

from datetime import datetime

from dateutil import relativedelta

import logger
import tools
from entry import Entry
from sql_client import SqlClient

log = logger.logger


class Splits:
    def __init__(self) -> None:
        self.base_link = "https://eresearch.fidelity.com/eresearch/conferenceCalls.jhtml?tab=splits&begindate={}"

    def __call__(self, ) -> None:
        today = datetime.today().date()
        today = today.replace(day=1)

        prev_month = (today - relativedelta.relativedelta(months=1)).strftime("%m/%d/%Y")
        curr_month = today.strftime("%m/%d/%Y")
        next_month = (today + relativedelta.relativedelta(months=1)).strftime("%m/%d/%Y")
        next_month_2 = (today + relativedelta.relativedelta(months=2)).strftime("%m/%d/%Y")

        for month in [prev_month, curr_month, next_month, next_month_2]:
            self.get_month_data(month)

    def get_month_data(self, month: str) -> None:
        log.info(f"Month -> {month}")
        link = self.base_link.format(month)
        soup = tools.prepare_soup(link)
        if not soup:
            log.warning("failed to fetch the page")
            return
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
                    symbol=symbol,
                    co_name=co_name,
                    ratio=ratio,
                    ann_date=ann_date,
                    rec_date=rec_date,
                    ex_date=ex_date,
                )
                if sql.insert_data(entry.sql_insert_data):
                    success += 1
            except Exception as e:
                log.error(e)
        else:
            log.info(f"{success} items saved to db")


if __name__ == "__main__":
    try:
        log.info("Script started")
        sql = SqlClient()
        if sql.initialize():
            scraper = Splits()
            scraper()
        else:
            log.critical("failed to establish connection with database.")
    except Exception as e:
        log.error(e)
    finally:
        if sql.connected:
            sql.close()
        log.info("Script ended")
