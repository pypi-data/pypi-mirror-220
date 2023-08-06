from typing import Sequence
from functools import lru_cache
from .log_support import logger
from .constant import CACHE_SIZE, Engin

_SHOW_SQL = False
_ENGIN = Engin.MySQL


def set_engin(engin: Engin):
    global _ENGIN
    _ENGIN = engin


def set_show_sql(show_sq: bool):
    global _SHOW_SQL
    _SHOW_SQL = show_sq


def before_execute(function: str, sql: str, *args):
    global _ENGIN
    global _SHOW_SQL
    if _SHOW_SQL:
        logger.info("Exec func 'mysqlx.db.%s' \n\tSQL: %s \n\tARGS: %s" % (function, sql, args))

    if _ENGIN == Engin.PostgreSQL and '%' in sql and 'like' in sql.lower():
        sql = sql.replace('%', '%%').replace('%%%%', '%%')

    return sql.replace('?', '%s')


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



