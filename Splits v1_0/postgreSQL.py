from typing import Tuple

import psycopg2

import logger
from tools import read_json

log = logger.logger
log.name = "PostgresSql"


class PostgreSql:
    def __init__(self) -> None:
        self.connected = False
        self.credential_filename = None

    def get_credentials(self) -> list:
        try:
            data = read_json(self.credential_filename)
            return data.values()
        except Exception as e:
            log.error(e)
            return [False] * 5

    def initialize(self):
        try:
            database, user, password, host, port = self.get_credentials()
            if not database:
                raise Exception
            self.conn = psycopg2.connect(
                database=database,
                user=user,
                password=password,
                host=host,
                port=port,
            )
            self.conn.autocommit = True
            self.connected = True
        except Exception as e:
            log.error(e)
        finally:
            return self.connected

    def _execute(self, query: str) -> bool:
        curr = self.conn.cursor()
        try:
            curr.execute(query)
        except Exception as e:
            log.error(e)
            self.conn.rollback()
            return False
        else:
            return True

    def select(self, table: str, columns: str = None, condition: str = None) -> Tuple[bool, list]:
        if condition:
            query = f"SELECT * FROM {table} WHERE {condition};"
        else:
            query = f"SELECT * FROM {table};"
        if columns:
            query = query.replace("*", columns)
        curr = self.conn.cursor()
        try:
            curr.execute(query)
        except Exception as e:
            log.error(e)
            log.error(query)
            self.conn.rollback()
            return None
        else:
            return curr.fetchall()

    def insert(self, table: str, insert_data: dict) -> bool:
        columns = ", ".join(insert_data.keys())
        values = ", ".join(insert_data.values())
        insert_query = f"""INSERT INTO {table} ({columns}) VALUES ({values});"""
        return self._execute(insert_query)
    
    def update(self, table: str, set: str, condition: str) -> bool:
        update_query = f"UPDATE {table} SET {set} WHERE {condition};"
        return self._execute(update_query)

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    pass
