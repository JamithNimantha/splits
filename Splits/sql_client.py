import os
from datetime import datetime
from typing import Optional

from dateutil import relativedelta
from psycopg2.extras import RealDictRow

from postgreSQL import PostgreSql


class SqlClient(PostgreSql):
    def __init__(self) -> None:
        super().__init__()
        self.credential_filename = f"Data{os.sep}Creadentals.json"
        self.table = 'public.splits'

    def already_exists(self, insert_data: dict) -> bool:
        condition = f"symbol={insert_data.pop('symbol')} and announcement_date={insert_data.pop('announcement_date')}"
        result = self.select(self.table, condition=condition)
        if result:
            return True

    def exists_in_base_min_vol_prc(self, insert_data: dict) -> bool:
        condition = f"symbol={insert_data.pop('symbol')}"
        result = self.select('base_min_vol_prc', condition=condition)
        if result:
            return True

    def find_by_symbol_in_base_min_vol_prc(self, symbol: str) -> Optional[RealDictRow]:
        condition = f"symbol='{symbol}'"
        records = self.select('base_min_vol_prc', condition=condition)
        if records:
            return records[0]
        return None

    def update_data(self, insert_data: dict) -> bool:
        condition = f"symbol={insert_data.pop('symbol')} and announcement_date={insert_data.pop('announcement_date')}"
        set_query = ''
        for key, val in insert_data.items():
            set_query += f"{key}={val}, "
        else:
            set_query = set_query[:-2]
        return self.update(self.table, set_query, condition)

    def insert_data(self, insert_data: dict) -> bool:
        if not self.exists_in_base_min_vol_prc(insert_data.copy()):
            return False
        if self.already_exists(insert_data.copy()):
            return self.update_data(insert_data)
        return self.insert(self.table, insert_data)

    def delete_old_data(self) -> bool:
        today = datetime.today().date()
        today = today.replace(day=1)
        date_from = (today - relativedelta.relativedelta(months=6)).strftime("%Y-%m-%d")
        condition = f"announcement_date < '{date_from}'"
        return self.delete(self.table, condition)
