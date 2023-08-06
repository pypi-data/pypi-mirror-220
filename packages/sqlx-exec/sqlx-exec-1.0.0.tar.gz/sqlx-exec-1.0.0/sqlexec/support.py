import threading
from .log_support import logger

DB_LOCK = threading.RLock()


def try_commit(db_ctx):
    if db_ctx.transactions == 0:
        logger.debug('Commit transaction...')
        try:
            db_ctx.connection.commit()
            logger.debug('Commit ok.')
        except Exception:
            logger.warning('Commit failed, try rollback...')
            db_ctx.connection.rollback()
            logger.warning('Rollback ok.')
            raise


class DBCtx(threading.local):
    """
    Thread local object that holds connection info.
    """

    def __init__(self, connect):
        self.connect = connect
        self.connection = None
        self.transactions = 0
        self.prepared = True
        self.get_cursor = lambda: self.connection.cursor()
        self.log = lambda action: logger.debug('%s connection <%s>...' % (action, hex(id(self.connection))))

    def is_not_init(self):
        return self.connection is None

    def init(self):
        self.transactions = 0
        self.connection = self.connect()
        self.log('Use')

    def release(self):
        if self.connection:
            self.log('Release')
            self.connection.close()
            self.connection = None

    def cursor(self):
        """
        Return cursor
        """
        # logger.debug('Cursor prepared: %s' % self.prepared)
        return self.get_cursor()

    def statement(self, sql: str):
        """
        Return statement
        """
        return self.connection.statement(sql)


class ConnectionCtx(object):
    """
    ConnectionCtx object that can open and close connection context. ConnectionCtx object can be nested and only the most
    outer connection has effect.
    with connection():
        pass
        with connection():
            pass
    """

    def __init__(self, db_ctx):
        self.db_ctx = db_ctx

    def __enter__(self):
        self.should_cleanup = False
        if self.db_ctx.is_not_init():
            self.db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exctype, excvalue, traceback):
        if self.should_cleanup:
            self.db_ctx.release()


class TransactionCtx(object):
    """
    TransactionCtx object that can handle transactions.
    with TransactionCtx():
        pass
    """

    def __init__(self, db_ctx):
        self.db_ctx = db_ctx

    def __enter__(self):
        self.should_close_conn = False
        if self.db_ctx.is_not_init():
            # needs open a connection first:
            self.db_ctx.init()
            self.should_close_conn = True
        self.db_ctx.transactions += 1
        logger.debug('Begin transaction...' if self.db_ctx.transactions == 1 else 'Join current transaction...')
        return self

    def __exit__(self, exctype, excvalue, traceback):
        self.db_ctx.transactions -= 1
        try:
            if self.db_ctx.transactions == 0:
                if exctype is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_close_conn:
                self.db_ctx.release()

    def commit(self):
        try_commit(self.db_ctx)

    def rollback(self):
        logger.warning('Rollback transaction...')
        self.db_ctx.connection.rollback()
        logger.debug('Rollback ok.')


class DBError(Exception):
    pass


class MultiColumnsError(DBError):
    pass


class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

