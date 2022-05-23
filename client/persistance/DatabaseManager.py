import sqlite3
from enum import Enum
from logging import info, debug
from sqlite3 import Cursor
from time import time
from typing import Optional, List

from client.persistance.Authorization import Authorization
from client.persistance.EventType import EventType
from client.persistance.types.User import User


class TableName(Enum):
    USERS = 'users'
    LOGS = 'logs'

    def __str__(self):
        return str(self.value)


class DatabaseManager:
    def __init__(self):
        debug("Establishing connection with database")
        self.conn = sqlite3.connect(
            'resources/database.sqlite', check_same_thread=False)
        self.c = self.conn.cursor()
        self.create_tables()

    def create_tables(self) -> None:
        self.c.execute(
            f'''CREATE TABLE IF NOT EXISTS logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at DATE NOT NULL,
                event_type VARCHAR(50) 
                    check (event_type in (
                    '{EventType.AUTHORIZED_ENTRANCE}',
                    '{EventType.DENIED_ENTRANCE}',
                    '{EventType.AUTHORIZED_LEAVE}',
                    '{EventType.DENIED_LEAVE}')
                    ) NOT NULL,
                tag_id INT NOT NULL
                )'''
        )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS users(
                tag_id INT PRIMARY KEY,
                is_authorized INT NOT NULL,
                created_at DATE NOT NULL
            )'''
        )

    def create_log(self, tag_id: int, event_type: EventType) -> None:
        self.c.execute(
            f"""INSERT INTO logs(created_at, event_type, tag_id) VALUES ({time()}, {event_type}, {tag_id})""")

    def create_or_update_user(self, tag_id: int, is_authorized: Authorization = Authorization.AUTHORIZED,
                              update_time: float = time()) -> None:
        self.c.execute(
            f'INSERT OR REPLACE INTO users(tag_id, is_authorized, created_at) '
            f'VALUES ({tag_id}, {is_authorized}, {update_time})'
        )
        self.conn.commit()

    def get_user(self, tag_id: int) -> Optional[User]:
        self.c.execute(f'SELECT * FROM users WHERE tag_id = {tag_id}')
        result = self.c.fetchone()

        if result is None:
            return None
        else:
            return User(result[0], Authorization.fromInt(result[1]), result[2])

    def is_tag_authorized(self, tag_id: int) -> bool:
        self.c.execute(
            f'SELECT is_authorized FROM users WHERE tag_id = {tag_id}')
        return self.c.fetchone()[0] == 1

    def print_users(self) -> None:
        info("=============USERS==============")
        for row in self.get_all(TableName.USERS):
            info(row)

    def print_logs(self) -> None:
        info("=============LOGS==============")
        for row in self.get_all(TableName.LOGS):
            info(row)

    def get_all(self, table_name: TableName) -> Cursor:
        return self.c.execute(f'SELECT * FROM {table_name}')

    def get_all_users(self) -> List[User]:
        users = self.c.execute(f'SELECT * FROM {TableName.USERS}')
        return list(map(lambda u: User(u[0], u[1], u[2]), users))
