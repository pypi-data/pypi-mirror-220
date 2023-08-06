from typing import Sequence
from functools import lru_cache
from .log_support import logger
from .engin import Engin

CACHE_SIZE = 256
_SHOW_SQL = False
_ENGIN = Engin.MySQL
before_execute = None


def insert_sql_args(table: str, **kwargs):
    cols, args = zip(*kwargs.items())
    sql = _create_insert_sql(table, cols)
    return sql, args


@lru_cache(maxsize=CACHE_SIZE)
def _create_insert_sql(table: str, cols: Sequence[str]):
    if _ENGIN == Engin.MySQL:
        columns, placeholders = zip(*[('`{}`'.format(col), '?') for col in cols])
        return 'INSERT INTO `{}`({}) VALUES({})'.format(table, ','.join(columns), ','.join(placeholders))

    columns, placeholders = zip(*[('{}'.format(col), '?') for col in cols])
    return 'INSERT INTO {}({}) VALUES({})'.format(table, ','.join(columns), ','.join(placeholders))


def get_batch_args(*args):
    return args[0] if isinstance(args, tuple) and len(args) == 1 and isinstance(args[0], Sequence) else args


def page_sql_args(sql: str, page_num=1, page_size=10, *args):
    global _ENGIN
    start = (page_num - 1) * page_size
    if require_limit(sql):
        if _ENGIN == Engin.MySQL:
            sql = '{} limit ?,?'.format(sql)
            args = [*args, start, page_size]
        elif _ENGIN == Engin.PostgreSQL:
            sql = '{} LIMIT ? OFFSET ?'.format(sql)
            args = [*args, page_size, start]
    return sql, args


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
    global _SHOW_SQL
    global before_execute
    _ENGIN = engin
    _ENGIN = engin
    _SHOW_SQL = show_sql
    if engin == Engin.PostgreSQL:
        if show_sql:
            before_execute =before_execute_postgres_show_sql
        else:
            before_execute = before_execute_postgres
    else:
        if show_sql:
            before_execute = before_execute_default_show_sql
        else:
            before_execute = lambda function, sql, *args: sql.replace('?', '%s')


def before_execute_default_show_sql(function: str, sql: str, *args):
    logger.info("Exec func 'sqlexec.%s' \n\tSQL: %s \n\tARGS: %s" % (function, sql, args))
    return sql.replace('?', '%s')


def before_execute_postgres(function: str, sql: str, *args):
    if '%' in sql and 'like' in sql.lower():
        sql = sql.replace('%', '%%').replace('%%%%', '%%')
    return sql.replace('?', '%s')


def before_execute_postgres_show_sql(function: str, sql: str, *args):
    logger.info("Exec func 'sqlexec.%s' \n\tSQL: %s \n\tARGS: %s" % (function, sql, args))
    if '%' in sql and 'like' in sql.lower():
        sql = sql.replace('%', '%%').replace('%%%%', '%%')
    return sql.replace('?', '%s')



