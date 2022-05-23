import os
from datetime import datetime
from typing import Optional, Tuple
from dateutil import parser
from dateutil import relativedelta
from psycopg2.extras import RealDictRow

from postgreSQL import PostgreSql


class SqlClient(PostgreSql):
    def __init__(self) -> None:
        super().__init__()
        self.credential_filename = f"Data{os.sep}Creadentals.json"
        self.table = 'public.splits'

    def already_exists(self, insert_data: dict) -> Tuple[bool, list]:
        condition = f"symbol={insert_data.pop('symbol')} and country={insert_data.pop('country')}"
        return self.select(self.table, condition=condition)

    def exists_in_base_min_vol_prc(self, insert_data: dict) -> bool:
        condition = f"symbol={insert_data.pop('symbol')}"
        result = self.select('base_min_vol_prc', condition=condition)
        if result:
            return True

    def delete_oldest_annoucement_date_if_duplicate_symbols_found(self, insert_data: dict) -> None:
        condition = f"symbol={insert_data['symbol']}"
        result = self.select(self.table, condition=condition, order=True)
        if result is not None and len(result) > 1:
            condition = f"symbol={insert_data['symbol']} and announcement_date > '{result[0]['announcement_date']}'"
            self.delete(self.table, condition)

    def find_by_symbol_in_base_min_vol_prc(self, symbol: str) -> Optional[RealDictRow]:
        condition = f"symbol='{symbol}'"
        records = self.select('base_min_vol_prc', condition=condition)
        if records:
            return records[0]
        return None

    def update_data(self, insert_data: dict, existing_record: RealDictRow) -> bool:
        condition = f"symbol={insert_data.pop('symbol')} and country={insert_data.pop('country')}"
        set_query = ''
        updated_split_from = float(insert_data['split_from'].replace("'", ""))
        updated_split_to = float(insert_data['split_to'].replace("'", ""))
        existing_split_from = float(existing_record['split_from'])
        existing_split_to = float(existing_record['split_to'])
        is_splits_ratio_updated: bool = False
        if updated_split_to >= existing_split_to:
            is_splits_ratio_updated = True
        else:
            is_splits_ratio_updated = False
        if updated_split_from >= existing_split_from:
            is_splits_ratio_updated = True
        else:
            is_splits_ratio_updated = False
        if is_splits_ratio_updated:
            insert_data.pop('split_from')
            insert_data.pop('split_to')
        for key, val in insert_data.items():
            if key.__contains__('date') and not key.__contains__('update'):
                if existing_record[key] is not None:
                    existing_date = datetime(year=existing_record[key].year, month=existing_record[key].month,
                                             day=existing_record[key].day)
                    updated_date = parser.parse(val.replace("to_timestamp('", '').replace("','yyyy-mm-dd')", ""))
                    if not updated_date < existing_date:
                        continue
            set_query += f"{key}={val}, "
        else:
            set_query = set_query[:-2]
        return self.update(self.table, set_query, condition)

    def insert_data(self, insert_data: dict) -> bool:
        if not self.exists_in_base_min_vol_prc(insert_data.copy()):
            return False
        existing_record = self.already_exists(insert_data.copy())
        if len(existing_record) > 0:
            rst = self.update_data(insert_data.copy(), existing_record[0])
            # self.delete_oldest_annoucement_date_if_duplicate_symbols_found(insert_data)
            return rst
        rst = self.insert(self.table, insert_data.copy())
        # self.delete_oldest_annoucement_date_if_duplicate_symbols_found(insert_data)
        return rst

    def delete_old_data(self) -> bool:
        today = datetime.today().date()
        # today = today.replace(day=1)
        date_from = (today - relativedelta.relativedelta(months=6)).strftime("%Y-%m-%d")
        condition = f"ex_date < '{date_from}'"
        return self.delete(self.table, condition)
