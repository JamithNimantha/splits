from postgreSQL import PostgreSql


class SqlClient(PostgreSql):
    def __init__(self) -> None:
        super().__init__()
        self.credential_filename = r"Data\Creadentals.json"
        self.table = 'public.splits'

    def already_exists(self, insert_data: dict) -> bool:
        condition = f"symbol={insert_data.pop('symbol')} and announcement_date={insert_data.pop('announcement_date')}"
        result = self.select(self.table, condition=condition)
        if result:
            return True

    def update_data(self, insert_data: dict) -> bool:
        condition = f"symbol={insert_data.pop('symbol')} and announcement_date={insert_data.pop('announcement_date')}"
        set_query = ''
        for key, val in insert_data.items():
            set_query += f"{key}={val}, "
        else:
            set_query = set_query[:-2]
        return self.update(self.table, set_query, condition)

    def insert_data(self, insert_data: dict) -> bool:
        if self.already_exists(insert_data.copy()):
            return self.update_data(insert_data)
        return self.insert(self.table, insert_data)
