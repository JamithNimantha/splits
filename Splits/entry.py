import datetime
from typing import Optional

from dateutil import parser


class Entry:
    def __init__(self, sql, **kwargs) -> None:
        self.sql = sql
        self.split_label = None
        self.update_time = None
        self.update_date = None
        self.note = None
        self.exchange = None
        self.optionable = None
        self.co_name = None
        self.split_from = None
        self.split_to = None
        self.updated_timestamp = None
        self.payable_date = None
        self.ex_date = None
        self.record_date = None
        self.announcement_date = None
        self.country = None
        self.symbol = None
        self.get(**kwargs)

    @property
    def json(self) -> dict:
        return self.__dict__

    def get(self, **kwargs) -> None:
        """
        Generator function.
        """
        symbol = kwargs['symbol']
        if symbol.__contains__(':'):
            if symbol.__contains__(':CA'):
                self.country = 'Canada'
            else:
                self.country = 'USA'
            self.symbol = symbol.replace(":CA", "").replace("/", ".").strip().upper()
        self.symbol = symbol
        self.exchange = kwargs['exchange']
        record = self.sql.find_by_symbol_in_base_min_vol_prc(self.symbol)
        if record is not None:
            if self.exchange is None:
                self.exchange = record['symbol']

        self.announcement_date = self.get_date(kwargs['ann_date'])
        self.record_date = self.get_date(kwargs['rec_date'])
        self.ex_date = self.get_date(kwargs['ex_date'])
        self.payable_date = self.get_date(kwargs['payable_date'])
        self.updated_timestamp = self.get_date(kwargs['updated_timestamp'])
        if kwargs['ratio'].endswith('%'):
            kwargs['ratio'] = f"{(int(kwargs['ratio'].replace('.000%', '')) * 0.01) + 1}:{1}"
        self.split_to, self.split_from = map(lambda x: round(float(x), 4), kwargs['ratio'].split(":"))
        if kwargs['co_name'] is not None:
            self.co_name = kwargs['co_name'].strip()
        self.note = kwargs['note']
        self.optionable = kwargs['optionable']
        self.update_date = self.get_date(str(datetime.datetime.today().date()))
        self.update_time = self.get_time(str(datetime.datetime.today().time()))
        if self.split_from > self.split_to:
            if self.record_date is None:
                self.split_label = f"RSPLIT|FRM:{self.split_from}|TO:{self.split_to}|DT:{kwargs['ann_date'].replace('/', '-')}|PAY:{kwargs['payable_date'].replace('/', '-')}|EX:{kwargs['ex_date'].replace('/', '-')}"
            else:
                self.split_label = f"RSPLIT|FRM:{self.split_from}|TO:{self.split_to}|DT:{kwargs['ann_date'].replace('/', '-')}|REC:{kwargs['rec_date'].replace('/', '-')}|EX:{kwargs['ex_date'].replace('/', '-')}"
        else:
            if self.record_date is None:
                self.split_label = f"SPLIT|FRM:{self.split_from}|TO:{self.split_to}|DT:{kwargs['ann_date'].replace('/', '-')}|PAY:{kwargs['payable_date'].replace('/', '-')}|EX:{kwargs['ex_date'].replace('/', '-')}"
            else:
                self.split_label = f"SPLIT|FRM:{self.split_from}|TO:{self.split_to}|DT:{kwargs['ann_date'].replace('/', '-')}|REC:{kwargs['rec_date'].replace('/', '-')}|EX:{kwargs['ex_date'].replace('/', '-')}"

    @staticmethod
    def get_date(date_: str) -> Optional[str]:
        if date_ in ['', None]:
            return None
        return f"to_timestamp('{parser.parse(date_)}','yyyy-mm-dd')"

    @staticmethod
    def get_time(date_: str) -> Optional[str]:
        if date_ in ['', None]:
            return None
        return f"to_timestamp('{date_}','HH24:M1:SS')::TIME"

    @property
    def sql_insert_data(self) -> dict:
        insert_data = {}
        for key, val in self.json.items():
            if val not in ['', None]:
                if key.__contains__('date') or key.__contains__('time'):
                    insert_data[key] = val
                elif type(val) == str:
                    insert_data[key] = f"""'{val.replace("'", "''")}'"""
                else:
                    insert_data[key] = f"""'{val}'"""
        return insert_data
