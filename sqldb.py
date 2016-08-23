import pymysql
import threading
from debug import log


def sql_log(sql, args=None):
    log.log_info('SQL: [%s] args: %s' % (sql, str(args or [])))


class Server:

    def __init__(self, **kw):
        self.host = kw.get('host', 'localhost')
        self.port = kw.get('port', 3306)
        self.user = kw['user']
        self.passwd = kw['password']
        self.db = kw['db']
        self.charset = kw.get('charset', 'utf8mb4')
        self.autocommit = kw.get('autocommit', True)
        self._connected = False
        self.mutex = threading.Lock()


        self.connect()


    def __lock(self):
        self.mutex.acquire()

    def __unlock(self):
        self.mutex.release()

        
    def connect(self):
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    password=self.passwd,
                                    db=self.db,
                                    charset=self.charset,
                                    autocommit=self.autocommit)

        self._connected = True
        return self._connected


    def __del__(self):
        self.connect = False
        self.conn.close()


    @property
    def connected(self):
        return self._connected
    # @connected.setter
    # def connected(self, value):
    #     self._connected = value

    # @classmethod
    def select(cls, sql, args, size=None):
        sql_log(sql, args)

        try:
            cls.__lock()
            with cls.conn.cursor() as cursor:
                cursor.execute(sql.replace('?', '%s'), args or ())
                if size:
                    rs = cursor.fetchmany(size)
                else:
                    rs = cursor.fetchall()
        finally:
            cursor.close()
            log.log_info('row returned: %s' %len(rs))
            cls.__unlock()
            return rs


    # @classmethod
    def execute(cls, sql, args):
        sql_log(sql, args)
        try:
            cls.__lock()
            with cls.conn.cursor() as cursor:
                cursor.execute(sql.replace('?', '%s'), args)
                affected = cursor.rowcount
                if not cls.autocommit:
                    cls.conn.commit()
        except BaseException as e:
            db.roolback()
            raise
        finally:
            cursor.close()
            cls.__unlock()
        return affected


if __name__ == '__main__':
    log()
    server = Server(user='mysqldb', password='mysqldb',db='sqldb')
    server.execute("INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)",
                               ('webmaster@python.org', 'very-secret'))

    rs = server.select("select `id`, `password` from `users` where `email`=?",
                  ('webmaster@python.org'))
    print(rs)



