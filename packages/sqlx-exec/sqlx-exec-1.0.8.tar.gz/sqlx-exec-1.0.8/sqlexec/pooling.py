from queue import Queue
from .support import DB_LOCK

MAX_POOL_SIZE = 32
_CONNECTION_POOL = None

def get_connect(conn_func, pool_size):
    global _CONNECTION_POOL
    assert 1 <= pool_size <= MAX_POOL_SIZE, 'pool_size should be higher or equal to 1 and lower or equal to {}'.format(MAX_POOL_SIZE)

    if _CONNECTION_POOL is None:
        with DB_LOCK:
            if _CONNECTION_POOL is None:
                _CONNECTION_POOL = ConnectionPool(conn_func, pool_size)

    return _CONNECTION_POOL.get_connection


class ConnectionPool:

    def __init__(self, conn_func, pool_size):
        self.connect = conn_func
        self.pool_size = pool_size
        self.pool_queue = Queue(pool_size)

        for _ in range(pool_size):
            self.add_connection()

    def add_connection(self, conn=None):
        if conn:
            self.pool_queue.put(conn, block=False)
        else:
            self.pool_queue.put(self.connect(), block=False)

    def get_connection(self):
        conn = self.pool_queue.get(timeout=1)
        return PooledConnection(self, conn)

    def close_all(self):
        for _ in  range(self.pool_size):
            try:
                self.pool_queue.get().close()
            except:
                pass


class PooledConnection(object):
    """Class holding a Connection in a pool

    PooledConnection is used by ConnectionPool to return an
    instance holding a connection. It works like a normal Connection
    except for methods like close()

    The close()-method will add the connection back to the pool rather
    than disconnecting from the MySQL server.
    """
    def __init__(self, pool, conn):
        """Initialize

        The pool argument must be an instance of ConnectionPoll. conn
        if an instance of Connection.
        """
        if not isinstance(pool, ConnectionPool):
            raise AttributeError(
                "pool should be a ConnectionPool")
        self._cnx_pool = pool
        self.conn = conn

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __getattr__(self, attr):
        """Calls attributes of the MySQLConnection instance"""
        return getattr(self.conn, attr)

    def close(self):
        """Do not close, but add connection back to pool

        The close() method does not close the connection with the
        MySQL server. The connection is added back to the pool so it
        can be reused.

        When the pool is configured to reset the session, the session
        state will be cleared by re-authenticating the user.
        """
        self._cnx_pool.add_connection(self.conn)
        self.conn = None
