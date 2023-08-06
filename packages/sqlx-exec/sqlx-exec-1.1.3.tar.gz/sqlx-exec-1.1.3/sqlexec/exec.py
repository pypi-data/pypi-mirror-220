import functools
from .engin import Engin
from . import sql_support
from .constant import MAPPER_PATH
from .log_support import logger, insert_log, save_log, get_log, page_log
from .support import DBCtx, ConnectionCtx, Dict, MultiColumnsError, TransactionCtx, try_commit, DBError, DB_LOCK

_DB_CTX = None


def init_db(connect=None, user='root', password='', database='test', host='127.0.0.1', port=3306, engin=Engin.MySQL, pool_size=1, show_sql=False, **kwargs):
    sql_support.set_config(engin, show_sql)
    if MAPPER_PATH in kwargs:
        del kwargs[MAPPER_PATH]

    if 'debug' in kwargs:
        if kwargs.pop('debug'):
            from logging import DEBUG
            logger.setLevel(DEBUG)

    if connect:
        import types
        assert isinstance(connect, types.FunctionType), '`connect` must be a function, you can use like `connect=lambda: connect(**kwargs)`.'
        _init_db(connect, engin, pool_size, pool_size)
    else:
        kwargs['user'] = user
        kwargs['password'] = password
        kwargs['database'] = database
        kwargs['host'] = host
        kwargs['port'] = port
        _import_init(engin, pool_size, **kwargs)


def _import_init(engin, pool_size, **kwargs):
    prepared = False
    real_size = pool_size

    if engin == Engin.MySQL:
        try:
            from mysql.connector import connect
            prepared = True
            if pool_size > 0:
                kwargs['pool_size'] = pool_size
                if 'pool_name' not in kwargs:
                    kwargs['pool_name'] = "{}_pool".format(kwargs.get('database'))
                pool_size = 0
        except ImportError:
            from pymysql import connect
    elif engin == Engin.PostgreSQL:
        from psycopg2 import connect
    else:
        raise DBError('Engin is invalid: %s', engin)

    _init_db(lambda: connect(**kwargs), engin, pool_size, real_size, prepared)


def _init_db(connect, engin, pool_size, real_size, prepared=False):
    global _DB_CTX
    with DB_LOCK:
        if _DB_CTX is not None:
            raise DBError('DB is already initialized.')
        if pool_size >= 1:
            from .pooling import pooled_connect
            connect = pooled_connect(connect, pool_size)
        _DB_CTX = DBCtx(connect=connect, pool_size=real_size, prepared=prepared)
    logger.info('Init db engine <%s> of %s with pool size: %d.' % (hex(id(_DB_CTX)), engin.value, real_size))


def connection():
    """
    Return _ConnectionCtx object that can be used by 'with' statement:
    with connection():
        pass
    """
    global _DB_CTX
    return ConnectionCtx(_DB_CTX)


def with_connection(func):
    """
    Decorator for reuse connection.
    @with_connection
    def foo(*args, **kw):
        f1()
        f2()
    """

    global _DB_CTX

    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with ConnectionCtx(_DB_CTX):
            return func(*args, **kw)

    return _wrapper


def transaction():
    """
    Create a transaction object so can use with statement:
    with transaction():
        pass
    with transaction():
         insert(...)
         update(... )
    """
    global _DB_CTX
    return TransactionCtx(_DB_CTX)


def with_transaction(func):
    """
    A decorator that makes function around transaction.
    @with_transaction
    def update_profile(id, name, rollback):
         u = dict(id=id, name=name, email='%s@test.org' % name, passwd=name, last_modified=time.time())
         insert('person', **u)
         r = update('update person set passwd=? where id=?', name.upper(), id)
    """
    global _DB_CTX

    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with TransactionCtx(_DB_CTX):
            return func(*args, **kw)

    return _wrapper


@with_connection
def execute(sql: str, *args):
    """
    Execute sql return effect rowcount
    sql: insert into person(name, age) values(?, ?)  -->  args: ('张三', 20)
    """
    global _DB_CTX
    cursor = None
    sql = sql_support.before_execute('execute', sql.strip(), *args)
    try:
        cursor = _DB_CTX.connection.cursor()
        cursor.execute(sql, args)
        effect_rowcount = cursor.rowcount
        try_commit(_DB_CTX)
        return effect_rowcount
    finally:
        if cursor:
            cursor.close()


def insert(table: str, **kwargs):
    """
    Insert data into table, return effect rowcount.
    :param table: table name
    :param kwargs: name='张三', age=20}
    return: Effect rowcount
    """
    insert_log('insert', table, **kwargs)
    sql, args = sql_support.insert_sql_args(table.strip(), **kwargs)
    return execute(sql, *args)


def save(select_key: str, table: str, **kwargs):
    """
    Insert data into table, return primary key.
    :param select_key: sql for select primary key
    :param table: table
    :param kwargs:
    :return: Primary key
    """
    save_log('save', select_key, table, **kwargs)
    sql, args = sql_support.insert_sql_args(table.strip(), **kwargs)
    return save_sql(select_key, sql, *args)


@with_connection
def save_sql(select_key: str, sql: str, *args):
    """
    Insert data into table, return primary key.
    :param select_key: sql for select primary key
    :param sql: table
    :param args:
    :return: Primary key
    """
    global _DB_CTX
    cursor = None
    logger.debug("Exec func 'sqlexec.%s', 'select_key': %s \n\t sql: %s \n\t args: %s" % ('save_sql', select_key, sql, args))
    sql = sql_support.before_execute('save_sql', sql, *args)
    try:
        cursor = _DB_CTX.connection.cursor()
        cursor.execute(sql, args)
        cursor.execute(select_key)
        result = cursor.fetchone()
        try_commit(_DB_CTX)
        return result[0]
    finally:
        if cursor:
            cursor.close()


def batch_insert(table: str, *args):
    """
    Batch insert
    :param table: table name
    :param args: All number must have same key. [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
    :return: Effect row count
    """
    logger.debug("Exec func 'sqlexec.%s' \n\t Table: '%s', args: %s" % ('batch_insert', table, args))
    assert len(args) > 0, 'args should not be empty.'
    sql, args = sql_support.batch_insert_sql_args(table, *args)
    return batch_execute(sql, *args)


@with_connection
def batch_execute(sql: str, *args):
    """
    Batch execute sql return effect rowcount
    :param sql: insert into person(name, age) values(?, ?)  -->  args: [('张三', 20), ('李四', 28)]
    :param args: All number must have same size.
    :return: Effect rowcount
    """
    global _DB_CTX
    cursor = None
    if isinstance(args[0], dict):
        sql, args = sql_support.batch_named_sql_args(sql, *args)
    sql = sql_support.before_execute('batch_execute', sql.strip(), *args)
    args = sql_support.get_batch_args(*args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.executemany(sql, args)
        effect_rowcount = cursor.rowcount
        try_commit(_DB_CTX)
        return effect_rowcount
    finally:
        if cursor:
            cursor.close()


def get(sql: str, *args):
    """
    Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    get_log('get', sql, *args)
    result = select_one(sql, *args)
    if result:
        if len(result) == 1:
            return result[0]
        msg = "Exec func 'sqlexec.%s' expect only one column but %d." % ('get', len(result))
        logger.error('%s  \n\t sql: %s \n\t args: %s' % (msg, sql, args))
        raise MultiColumnsError(msg)
    return None


@with_connection
def select(sql: str, *args):
    """
    execute select SQL and return unique result or list results(tuple).
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    global _DB_CTX
    cursor = None
    sql = sql_support.before_execute('select', sql.strip(), *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()


@with_connection
def select_one(sql: str, *args):
    """
    Execute select SQL and return unique result(tuple), SQL contain 'limit'.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    global _DB_CTX
    cursor = None
    sql = sql_support.before_execute('select_one', sql.strip(), *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()


def select_page(sql: str, page_num, page_size, *args):
    page_log('select_page', sql.strip(), page_num, page_size, args)
    sql, args = sql_support.page_sql_args(sql, page_num, page_size, *args)
    return select(sql, *args)


@with_connection
def query(sql: str, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    global _DB_CTX
    cursor = None
    sql = sql_support.before_execute('query', sql.strip(), *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        results = cursor.fetchall()
        if results and cursor.description:
            names = [x[0] for x in cursor.description]
            return [Dict(names, x) for x in results]
        else:
            return results
    finally:
        if cursor:
            cursor.close()


@with_connection
def query_one(sql: str, *args):
    """
    execute select SQL and return unique result(dict), SQL contain 'limit'.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    global _DB_CTX
    cursor = None
    sql = sql_support.before_execute('query_one', sql.strip(), *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        if result and cursor.description:
            names = [x[0] for x in cursor.description]
            return Dict(names, result)
        return result
    finally:
        if cursor:
            cursor.close()


def query_page(sql: str, page_num, page_size, *args):
    page_log('query_page', sql.strip(), page_num, page_size, args)
    sql, args = sql_support.page_sql_args(sql, page_num, page_size, *args)
    return query(sql, *args)


def get_connection():
    global _DB_CTX
    if _DB_CTX.is_not_init():
        _DB_CTX.init()
    return _DB_CTX.connection

