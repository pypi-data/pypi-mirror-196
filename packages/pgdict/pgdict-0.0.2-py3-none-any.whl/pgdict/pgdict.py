import psycopg2
from psycopg2.extras import Json
from psycopg2.sql import Identifier, SQL
from collections import UserDict
from dataclasses import dataclass


class KeyNotFound(Exception):
    pass


@dataclass
class ConnectionConfig:
    database: str
    table: str
    user: str
    password: str
    host: str
    port: int


class Transaction:
    def __init__(self, store):
        self.store = store
        self.conn = store.manager.conn

    def __enter__(self):
        self.conn.autocommit = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.autocommit = True


def reconnect_and_retry(method):
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except psycopg2.Error:
            if self.conn.closed != 0:
                # 0 - connection is open
                # 1 - connection has been closed
                # 2 - something horrible has happened
                self.reconnect()
                return method(self, *args, **kwargs)
            else:
                raise

    return wrapper


class OperationsMixin:
    @reconnect_and_retry
    def get(self, key):
        cur = self.conn.cursor()
        sql = SQL("SELECT value FROM {TABLE} WHERE key=%(key)s").format(
            TABLE=Identifier(self.table)
        )
        cur.execute(sql, {"key": key})
        value = cur.fetchone()
        cur.close()
        if value is None:
            raise KeyNotFound
        return value[0]

    @reconnect_and_retry
    def get_items(self, keys=None):
        cur = self.conn.cursor()
        if keys:
            sql = SQL("SELECT key, value FROM {TABLE} WHERE key=ANY(%(keys)s)").format(
                TABLE=Identifier(self.table)
            )
        else:
            sql = SQL("SELECT key, value FROM {TABLE}").format(
                TABLE=Identifier(self.table)
            )
        cur.execute(sql, {"keys": keys})
        values = cur.fetchall()
        cur.close()
        return values

    @reconnect_and_retry
    def exists(self, key):
        cur = self.conn.cursor()
        sql = SQL("SELECT 1 FROM {TABLE} WHERE key=%(key)s").format(
            TABLE=Identifier(self.table)
        )
        cur.execute(sql, {"key": key})
        exists = cur.fetchone() is not None
        cur.close()
        return exists

    @reconnect_and_retry
    def put(self, key, value) -> None:
        cur = self.conn.cursor()
        sql = SQL(
            """
            INSERT INTO {TABLE} (key, value)
            VALUES (%(key)s, %(value)s)
            ON CONFLICT (key) DO UPDATE SET value = %(value)s
        """
        ).format(TABLE=Identifier(self.table))
        cur.execute(sql, {"key": key, "value": Json(value)})
        cur.close()

    @reconnect_and_retry
    def delete(self, key):
        if not self.exists(key):
            raise KeyNotFound
        cur = self.conn.cursor()
        sql = SQL("DELETE FROM {TABLE} WHERE key=%(key)s").format(
            TABLE=Identifier(self.table)
        )
        cur.execute(sql, {"key": key})
        cur.close()

    @reconnect_and_retry
    def key_count(self):
        cur = self.conn.cursor()
        sql = SQL("SELECT COUNT(*) FROM {TABLE}").format(TABLE=Identifier(self.table))
        cur.execute(sql)
        count = cur.fetchone()[0]
        cur.close()
        return count


class StoreManager(OperationsMixin):
    """Keys must be strings"""

    def __init__(self, config: ConnectionConfig):
        self.config = config
        self.conn = psycopg2.connect(
            database=config.database,
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
        )
        self.conn.autocommit = True
        self.table = config.table

    def reconnect(self):
        self.conn.close()
        self.conn = psycopg2.connect(
            database=self.config.database,
            user=self.config.user,
            password=self.config.password,
            host=self.config.host,
            port=self.config.port,
        )

    def close_connection(self):
        self.conn.close()


class Store(UserDict):
    """Keys must be strings"""

    def __init__(self, config: ConnectionConfig):
        self.manager = StoreManager(config)

    def __getitem__(self, key):
        try:
            return self.manager.get(key)
        except KeyNotFound:
            raise KeyError

    def __contains__(self, key):
        return self.manager.exists(key)

    def __setitem__(self, key, value):
        self.manager.put(key, value)

    def __delitem__(self, key):
        self.manager.delete(key)

    def __iter__(self):
        return iter(self.manager.keys())

    def __len__(self):
        return self.manager.key_count()

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def items(self):
        return self.manager.get_items()

    def keys(self):
        return [key for key, _ in self.items()]

    def values(self):
        return [value for _, value in self.items()]

    def disconnect(self):
        self.manager.close_connection()
