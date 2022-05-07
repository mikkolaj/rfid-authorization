import sqlite3
from enum import Enum
from logging import info, debug
from time import time

from client.persistance.EventType import EventType


class TableName(Enum):
    USERS = 'users',
    LOGS = 'logs'


class DatabaseManager:
    def __init__(self):
        debug("Establishing connection with database")
        self.conn = sqlite3.connect('resources/database.sqlite')
        self.c = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.c.execute(f'''
            CREATE TABLE IF NOT EXISTS logs(
                id INT PRIMARY KEY,
                created_at DATE NOT NULL,
                event_type VARCHAR(50) 
                    check (event_type in (
                    '{EventType.AUTHORIZED_ENTRANCE}',
                    '{EventType.DENIED_ENTRANCE}',
                    '{EventType.AUTHORIZED_LEAVE}',
                    '{EventType.DENIED_LEAVE}')
                    ) NOT NULL,
                tag_id INT UNIQUE NOT NULL )'''
                       )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS users(
                tag_id INT PRIMARY KEY,
                is_authorized INT NOT NULL,
                created_at DATE NOT NULL
        )
        ''')

    def create_log(self, tag_id, event_type: EventType):
        self.c.execute(f"""INSERT INTO logs VALUES ({time()}, {event_type}, {tag_id})""")

    # def create_user(self, tag_id):
    #     self.c.execute(
    #         f"""INSERT INTO users(tag_id, is_authorized, created_at) VALUES ({tag_id}, 1, {time()})""")
    #     self.conn.commit()
    #
    # def modify_user(self, tag_id, is_authorized):
    #     self.c.execute(f'SELECT COUNT(*) FROM users WHERE tag_id = {tag_id}')
    #     is_user_present = self.c.fetchone()[0]
    #
    #     if is_user_present > 0:
    #         self.c.execute(
    #             f"UPDATE users SET is_authorized = {is_authorized}, created_at = {time()} WHERE tag_id = {tag_id}")
    #         self.conn.commit()
    #     else:
    #         self.create_user(tag_id)

    def create_or_update_user(self, tag_id, is_authorized=True):
        self.c.execute(
            f'INSERT OR REPLACE INTO users(tag_id, is_authorized, created_at) '
            f'VALUES ({tag_id}, {is_authorized}, {time()})'
        )
        self.conn.commit()

    def is_tag_authorized(self, tag_id):
        self.c.execute(f'SELECT is_authorized FROM users WHERE tag_id = {tag_id}')
        return self.c.fetchone()[0] == 1

    def print_users(self):
        info("=============USERS==============")
        for row in self.get_all():
            info(row)

    def print_logs(self):
        info("=============LOGS==============")
        for row in self.get_all():
            info(row)

    def get_all(self, table_name):
        return self.c.execute(f'SELECT * FROM {table_name}')
