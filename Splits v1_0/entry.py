from dateutil import parser


class Entry:
    def __init__(self, **kwargs) -> None:
        self.get(**kwargs)

    @property
    def json(self) -> dict:
        return self.__dict__

    def get(self, **kwargs) -> object:
        """
        Generator function.
        """
        symbol = kwargs['symbol']
        if symbol.__contains__(':CA'):
            self.country = 'Canada'
        else:
            self.country = 'USA'
        self.symbol = symbol.replace(":CA", "").replace("/", ".").strip().upper()
        self.announcement_date = self.get_date(kwargs['ann_date'])
        self.record_date = self.get_date(kwargs['rec_date'])
        self.ex_date = self.get_date(kwargs['ex_date'])

        self.split_to, self.split_from = map(lambda x: round(float(x), 4), kwargs['ratio'].split(":"))
        self.co_name = kwargs['co_name'].strip()
        if self.split_from > self.split_to:
            self.split_label = f"RSPLIT|FRM:{self.split_from}|TO:{self.split_to}|DT:{kwargs['ann_date'].replace('/', '-')}|REC:{kwargs['rec_date'].replace('/', '-')}|EX:{kwargs['ex_date'].replace('/', '-')}"
        else:
            self.split_label = f"SPLIT|FRM:{self.split_from}|TO:{self.split_to}|DT:{kwargs['ann_date'].replace('/', '-')}|REC:{kwargs['rec_date'].replace('/', '-')}|EX:{kwargs['ex_date'].replace('/', '-')}"

    def get_date(self, date_: str) -> None:
        return f"to_timestamp('{parser.parse(date_)}','yyyy-mm-dd')"

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
