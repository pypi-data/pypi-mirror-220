import re
from enum import Enum
from typing import Sequence
from functools import lru_cache
from .log_support import logger
from .constant import CACHE_SIZE


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
    @lru_cache(maxsize=CACHE_SIZE)
    def create_insert_sql(table: str, cols: Sequence[str]):
        columns, placeholders = zip(*[('`{}`'.format(col), '?') for col in cols])
        return 'INSERT INTO `{}`({}) VALUES({})'.format(table, ', '.join(columns), ','.join(placeholders))

    @staticmethod
    def page_sql_args(require_limit, sql: str, start, page_size, *args):
        if require_limit(sql):
            sql = '{} limit ?, ?'.format(sql)
        args = [*args, start, page_size]
        return sql, args

    @staticmethod
    def get_select_key(*args, **kwargs):
        return "SELECT LAST_INSERT_ID()"


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
    def get_select_key(pk_seq: str, sql: str, *args, **kwargs):
        if not pk_seq:
            pk_seq = _get_pk_seq_from_sql(sql)
        return f"SELECT currval('{pk_seq}')"


@lru_cache(maxsize=CACHE_SIZE)
def _get_pk_seq_from_sql(sql: str):
    table = re.search('(?<=into )\w+', sql, re.I)
    pk_seq = "{}_id_seq".format(table.group())
    logger.warning("'pk_seq' is None, will use default '{}' from sql.".format(pk_seq))
    return pk_seq
