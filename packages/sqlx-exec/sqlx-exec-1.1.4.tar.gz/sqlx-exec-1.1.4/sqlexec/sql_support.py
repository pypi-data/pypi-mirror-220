import re
from typing import Sequence
from functools import lru_cache
from .engin import create_sql_engin
from .constant import CACHE_SIZE, NAMED_REGEX

_ENGIN = None
_SQL_ENGIN = None
before_execute = None


def get_select_key(*args, **kwargs):
    global _SQL_ENGIN
    return _SQL_ENGIN.get_select_key(*args, **kwargs)


def get_column_sql():
    global _SQL_ENGIN
    return _SQL_ENGIN.get_column_sql()


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
    sql = _SQL_ENGIN.create_insert_sql(table, cols[0])
    return sql, args


def batch_named_sql_args(sql: str, *args):
    args = get_batch_args(*args)
    args = [get_named_args(sql, **arg) for arg in args]
    sql = get_named_sql(sql)
    return sql, args


@lru_cache(maxsize=CACHE_SIZE)
def get_named_sql(sql: str):
    return re.sub(NAMED_REGEX, '?', sql)


def get_named_args(sql: str, **kwargs):
    return [kwargs[r[1:]] for r in re.findall(NAMED_REGEX, sql)]


def page_sql_args(sql: str, page_num=1, page_size=10, *args):
    global _SQL_ENGIN
    start = (page_num - 1) * page_size
    return _SQL_ENGIN.page_sql_args(require_limit, sql, start, page_size, *args)


def require_limit(sql: str):
    lower_sql = sql.lower()
    if 'limit' not in lower_sql:
        return True
    idx = lower_sql.rindex('limit')
    if idx > 0 and ')' in lower_sql[idx:]:
        return True
    return False


def set_config(engin, show_sql):
    global _ENGIN
    global _SQL_ENGIN
    global before_execute
    _ENGIN = engin
    _SQL_ENGIN = create_sql_engin(engin, show_sql)
    before_execute = _SQL_ENGIN.before_execute


def get_engin():
    global _ENGIN
    return _ENGIN


# def get_sql_engin():
#     global _SQL_ENGIN
#     return _SQL_ENGIN