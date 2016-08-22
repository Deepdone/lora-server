import debug
import aiomysql


def sql_log(sql, args=None):
    debug.log_info('SQL: [%s] args: %s' % (sql, str(args or []])))


class Server:

    def __init__(self, **kw):
        self.host = kw.get('host', 'localhost'),
        self.port = kw.get('port', self.default_port),
        self.user = kw['user'],
        self.passwd = kw['password'],
        self.db = kw['db'],
        self.charset = kw.get('charset', 'utf8'),
        self.autocommit = kw.get('autocommit', True),
        self._connected = False

        
    async def connect(self):
        self.conn = await aiomysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.passwd,
            db = self.db,
            charset = self.charset,
            autocommit = self.autocommit
            )
        self._connected = True
        return self._connected


    def __del__(self):
        self.__class__.disconnect()

    async def disconnect(self):
        self.connect = False
        self.conn.close()
        await self.conn.closed()

    @property
    def connected(self):
        return self._connected
    # @connected.setter
    # def connected(self, value):
    #     self._connected = value
    
    async def __select(self, sql, args, size=None):
        sql_log(sql, args)
        cur = await self.conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        debug.log_info('row returned: %s' %len(rs))


    async def __execute(self, sql, args):
        sql_log(sql, args)
        try:
            cur = await self.conn.cursor()
            await cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount
            await cur.close()
        except BaseException as e:
            raise
        return affected

    @classmethod
    async def create_pool(self, loop, **kw):
        sql_log('create database connection pool...')
        global __pool
        __pool = await aiomysql.create_pool(
            host = kw.get('host', 'localhost'),
            port = kw.get('port', self.default_port),
            user = kw['user'],
            password = kw['password'],
            db = kw['db'],
            charset = kw.get('charset', 'utf8'),
            autocommit = kw.get('autocommit', True),
            maxsize = kw.get('maxsize', 10),
            minsize = kw.get('minsize', 1),
            loop = loop
        )

    @classmethod
    async def close_pool(self):
        sql_log('close database connection pool...')
        global __pool
        __pool.close()
        await __pool.wait_closed()



