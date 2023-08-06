from logging import basicConfig, INFO, getLogger

logger = getLogger(__name__)
basicConfig(level=INFO, format='[%(levelname)s]: %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def insert_log(function: str, table: str, **kwargs):
    logger.debug("Exec func 'sqlexec.%s' \n\t Table: '%s', kwargs: %s" % (function, table, kwargs))


def do_sql_log(function: str, sql: str, *args):
    logger.debug("Exec func 'sqlexec.%s' \n\t sql: %s \n\t args: %s" % (function, sql, args))

