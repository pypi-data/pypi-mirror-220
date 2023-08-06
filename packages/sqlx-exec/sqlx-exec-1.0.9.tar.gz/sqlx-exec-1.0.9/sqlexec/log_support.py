from logging import basicConfig, INFO, getLogger

logger = getLogger(__name__)
basicConfig(level=INFO, format='[%(levelname)s]: %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def insert_log(function: str, table: str, **kwargs):
    logger.debug("Exec func 'sqlexec.%s' \n\t Table: '%s', kwargs: %s" % (function, table, kwargs))


def save_log(function: str, pk_sql: str, table: str, **kwargs):
    logger.debug("Exec func 'sqlexec.%s', 'pk_sql': %s \n\t Table: '%s', kwargs: %s" % (function, pk_sql, table, kwargs))


def get_log(function: str, sql: str, *args):
    logger.debug("Exec func 'sqlexec.%s' \n\t sql: %s \n\t args: %s" % (function, sql, args))


def page_log(function: str, sql: str, page_num, page_size, *args):
    logger.debug("Exec func 'sqlexec.%s', page_num: %d, page_size: %d \n\t sql: %s \n\t args: %s" % (function, page_num, page_size, sql, args))


def db_ctx_log(action, connection):
    logger.debug('%s connection <%s>...' % (action, hex(id(connection))))

