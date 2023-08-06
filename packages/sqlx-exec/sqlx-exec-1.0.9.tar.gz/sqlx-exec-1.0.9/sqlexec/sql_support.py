from typing import Sequence
from .log_support import logger
from .engin import Engin, MySqlEngin, PostgresEngin

CACHE_SIZE = 256
_SQL_ENGIN = None
before_execute = None


def insert_sql_args(table: str, **kwargs):
    cols, args = zip(*kwargs.items())
    sql = _SQL_ENGIN.create_insert_sql(table, cols)
    return sql, args


def get_batch_args(*args):
    return args[0] if isinstance(args, tuple) and len(args) == 1 and isinstance(args[0], Sequence) else args


def batch_insert_sql_args(table: str, *args):
    args = get_batch_args(*args)
    args = [zip(*arg.items()) for arg in args]  # [(cols, args)]
    cols, args = zip(*args)  # (cols), (args)
    sql = _SQL_ENGIN.create_insert_sql(table, cols)
    return sql, args


def page_sql_args(sql: str, page_num=1, page_size=10, *args):
    global _SQL_ENGIN
    start = (page_num - 1) * page_size
    return _SQL_ENGIN.page_sql_args(require_limit, sql, start, page_size, *args)


def get_pk_sql(*args):
    global _SQL_ENGIN
    return _SQL_ENGIN.pk_sql(*args)


def require_limit(sql: str):
    lower_sql = sql.lower()
    if 'limit' not in lower_sql:
        return True
    idx = lower_sql.rindex('limit')
    if idx > 0 and ')' in lower_sql[idx:]:
        return True
    return False


def set_config(engin, show_sql):
    global _SQL_ENGIN
    global before_execute
    if engin == Engin.MySQL:
        _SQL_ENGIN = MySqlEngin(logger, show_sql)
    elif engin == Engin.PostgreSQL:
        _SQL_ENGIN = PostgresEngin(logger, show_sql)
    before_execute = _SQL_ENGIN.before_execute




