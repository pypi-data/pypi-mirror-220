from enum import Enum
from typing import Sequence
from functools import lru_cache

CACHE_SIZE = 256


class Engin(Enum):
    MySQL = 'MySQL'
    PostgreSQL = 'PostgreSQL'


class SqlEngin:
    def __init__(self, logger, show_sql):
        self.logger = logger
        self.show_sql = show_sql

    def before_execute(self, function: str, sql: str, *args):
        if self.show_sql:
            self.logger.info("Exec func 'sqlexec.%s' \n\tSQL: %s \n\tARGS: %s" % (function, sql, args))
        return sql.replace('?', '%s')

    @staticmethod
    @lru_cache(maxsize=CACHE_SIZE)
    def create_insert_sql(table: str, cols: Sequence[str]):
        columns, placeholders = zip(*[('{}'.format(col), '?') for col in cols])
        return 'INSERT INTO {}({}) VALUES({})'.format(table, ', '.join(columns), ','.join(placeholders))


class MySqlEngin(SqlEngin):

    def __init__(self, logger, show_sql):
        super().__init__(logger, show_sql)

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
    def get_select_key(*args):
        return "SELECT LAST_INSERT_ID()"


class PostgresEngin(SqlEngin):

    def __init__(self, logger, show_sql):
        super().__init__(logger, show_sql)

    def before_execute(self, function: str, sql: str, *args):
        if self.show_sql:
            self.logger.info("Exec func 'sqlexec.%s' \n\tSQL: %s \n\tARGS: %s" % (function, sql, args))
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
    def get_select_key(pk_seq, *args):
        return  "SELECT currval('{}')".format(pk_seq)
