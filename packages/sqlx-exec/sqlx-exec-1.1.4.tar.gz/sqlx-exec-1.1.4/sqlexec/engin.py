import re
from enum import Enum
from typing import Sequence
from .support import DBError
from functools import lru_cache
from .log_support import logger
from .constant import CACHE_SIZE, MYSQL_COLUMN_SQL, POSTGRES_COLUMN_SQL


def create_sql_engin(engin, show_sql):
    if engin == Engin.MySQL:
        return MySqlEngin(show_sql)
    elif engin == Engin.PostgreSQL:
        return PostgresEngin(show_sql)
    raise


class Engin(Enum):
    MySQL = 'MySQL'
    PostgreSQL = 'PostgreSQL'


class SqlEngin:
    def __init__(self, show_sql):
        self.show_sql = show_sql

    def before_execute(self, function: str, sql: str, *args):
        if self.show_sql:
            logger.info("Exec func 'sqlexec.%s' \n\tSQL: %s \n\tARGS: %s" % (function, sql, args))
        if '%' in sql and 'like' in sql.lower():
            sql = sql.replace('%', '%%').replace('%%%%', '%%')
        return sql.replace('?', '%s')

    @staticmethod
    @lru_cache(maxsize=CACHE_SIZE)
    def create_insert_sql(table: str, cols: Sequence[str]):
        columns, placeholders = zip(*[('{}'.format(col), '?') for col in cols])
        return 'INSERT INTO {}({}) VALUES({})'.format(table, ', '.join(columns), ','.join(placeholders))


class MySqlEngin(SqlEngin):

    def __init__(self, show_sql):
        super().__init__(show_sql)

    @staticmethod
    def page_sql_args(require_limit, sql: str, start, page_size, *args):
        if require_limit(sql):
            sql = '{} limit ?, ?'.format(sql)
        args = [*args, start, page_size]
        return sql, args

    @staticmethod
    def get_select_key(*args, **kwargs):
        return "SELECT LAST_INSERT_ID()"

    @staticmethod
    def get_column_sql():
        return MYSQL_COLUMN_SQL




class PostgresEngin(SqlEngin):

    def __init__(self, show_sql):
        super().__init__(show_sql)

    def before_execute(self, function: str, sql: str, *args):
        if self.show_sql:
            logger.info("Exec func 'sqlexec.%s' \n\tSQL: %s \n\tARGS: %s" % (function, sql, args))
        if '%' in sql and 'like' in sql.lower():
            sql = sql.replace('%', '%%').replace('%%%%', '%%')
        return sql.replace('?', '%s')

    @staticmethod
    def page_sql_args(require_limit, sql: str, start, page_size, *args):
        if require_limit(sql):
            sql = '{} LIMIT ? OFFSET ?'.format(sql)
        args = [*args, page_size, start]
        return sql, args

    @staticmethod
    def get_select_key(pk_seq: str = None, table: str = None, sql: str = None, *args, **kwargs):
        if not pk_seq:
            if table:
                pk_seq = PostgresEngin._build_pk_seq(table)
            else:
                if sql:
                    pk_seq = PostgresEngin._get_pk_seq_from_sql(sql)
                else:
                    raise DBError("Get PostgreSQL select key fail, all of 'pk_seq', 'table', 'sql' are None")
        return f"SELECT currval('{pk_seq}')"

    @staticmethod
    def get_column_sql():
        return POSTGRES_COLUMN_SQL

    @staticmethod
    def _build_pk_seq(table: str):
        return f'{table}_id_seq'

    @staticmethod
    @lru_cache(maxsize=CACHE_SIZE)
    def _get_pk_seq_from_sql(sql: str):
        table = re.search('(?<=into )\w+', sql, re.I)
        pk_seq = PostgresEngin._build_pk_seq(table.group())
        logger.warning("'pk_seq' is None, will use default '{}' from sql.".format(pk_seq))
        return pk_seq
