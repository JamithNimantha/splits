import datetime
from typing import Optional

from dateutil import parser

__version__ = 1.1
__author__ = 'Jamith Nimantha'


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
        self.country = 'USA'
        if symbol.__contains__(':'):
            if symbol.__contains__(':CA'):
                self.country = 'Canada'
            symbol = symbol.replace(":CA", "").replace("/", ".").strip().upper()
        self.symbol = symbol
        self.exchange = kwargs['exchange']
        self.announcement_date = self.get_date(kwargs['ann_date'])
        self.record_date = self.get_date(kwargs['rec_date'])
        self.ex_date = self.get_date(kwargs['ex_date'])
        if self.ex_date is None:
            raise Exception('ex_date is empty for {}'.format(self.symbol))
        self.payable_date = self.get_date(kwargs['payable_date'])
        # self.updated_timestamp = self.get_date(kwargs['updated_timestamp'])
        if kwargs['ratio'].endswith('%'):
            kwargs['ratio'] = f"{(float(kwargs['ratio'].replace('%', '')) * 0.01) + 1}:{1}"
        if kwargs['ratio'] == '':
            raise Exception('Ratio is empty for {}'.format(self.symbol))
        self.split_to, self.split_from = map(lambda x: round(float(x), 4), kwargs['ratio'].split(":"))
        if kwargs['co_name'] is not None:
            self.co_name = kwargs['co_name'].strip()
        self.note = kwargs['note']
        self.optionable = kwargs['optionable']
        self.update_date = self.get_date(str(datetime.datetime.today().date()))
        self.update_time = self.get_time(str(datetime.datetime.today().time()))
        if self.split_from > self.split_to:
            self.split_label = f"RSPLIT|FRM:{self.split_from}|TO:{self.split_to}"
        else:
            self.split_label = f"SPLIT|FRM:{self.split_from}|TO:{self.split_to}"
        if self.announcement_date is not None:
            self.split_label += f"|DT:{self.get_date_for_label(kwargs['ann_date'])}"
        if self.payable_date is not None:
            self.split_label += f"|PAY:{self.get_date_for_label(kwargs['payable_date'])}"
        if self.record_date is not None:
            self.split_label += f"|REC:{self.get_date_for_label(kwargs['rec_date'])}"
        if self.ex_date is not None:
            self.split_label += f"|EX:{self.get_date_for_label(kwargs['ex_date'])}"

    @staticmethod
    def get_date(date_: str) -> Optional[str]:
        if date_ in ['', None]:
            return None
        return f"to_timestamp('{parser.parse(date_)}','yyyy-mm-dd')"

    @staticmethod
    def get_date_for_label(date_: str) -> Optional[str]:
        # 29 - Jun - 22
        return parser.parse(date_).strftime("%d-%b-%y")

    @staticmethod
    def get_time(date_: str) -> Optional[str]:
        if date_ in ['', None]:
            return None
        return f"to_timestamp('{date_}','HH24:MI:SS')::TIME"

    @property
    def sql_insert_data(self) -> dict:
        insert_data = {}
        for key, val in self.json.items():
            if val not in ['', None]:
                if key.__contains__('date') or key.__contains__('time'):
                    insert_data[key] = val
                elif key.__contains__('sql'):
                    pass
                elif type(val) == str:
                    insert_data[key] = f"""'{val.replace("'", "''")}'"""
                else:
                    insert_data[key] = f"""'{val}'"""
        return insert_data
