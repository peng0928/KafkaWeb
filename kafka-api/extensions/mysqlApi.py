import pymysql
from pymysql.converters import escape_string
from logs.settings import loggers

loguer = loggers


def ErrorTip(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            loguer.error(e)

    return wrapper


class PrMysql(object):
    """
    数据存储
    """

    def __init__(
            self, host='localhost', port=3306, user=None,
            password=None, db=None, charset=None, tb=None, tip=False, loguer=loguer, **kwargs):
        """
        创建连接
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.tip = tip
        self.kwargs = kwargs
        self.pyconn = pymysql.connect(host=host, port=port, user=user, password=password,
                                      database=db, charset=charset, **kwargs)
        self.tip = tip
        self.loguer = loguer
        self.table = tb
        self.login('[%s]数据库成功连接' % db)

    @property
    @ErrorTip
    def conn(self):
        pyconn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                 database=self.db, charset=self.charset, **self.kwargs)
        return pyconn

    @property
    @ErrorTip
    def cursor(self):
        pyconn = self.conn
        cursor = pyconn.cursor()
        return cursor

    @ErrorTip
    def insert(self, sql):
        pyconn = self.conn
        cursor = pyconn.cursor()
        cursor.execute(sql)
        insert_id = pyconn.insert_id()
        self.login('数据成功插入: %s' % insert_id)
        pyconn.commit()
        return insert_id

    @ErrorTip
    def execute(self, sql):
        pyconn = self.conn
        cursor = pyconn.cursor()
        cursor.execute(sql)
        pyconn.commit()

    @ErrorTip
    def select(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchone()

    @ErrorTip
    def selectall(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @ErrorTip
    def selectmany(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchmany()

    @ErrorTip
    def executemany(self, sql):
        return self.cursor.executemany(sql)

    def save(self, **kwargs):
        sql = self.dict_to_sql(**kwargs)
        self.insert(sql)

    def login(self, e):
        self.loguer.info(e) if self.tip else None

    def logerr(self, e):
        self.loguer.error(e) if self.tip else None

    def dict_to_sql(self, **kwargs):
        from pymysql.converters import escape_string
        columns = []
        values = []
        for key, value in kwargs.items():
            columns.append(key)
            values.append(value)
        columns = ','.join(columns)
        values = ','.join(['"%s"' % escape_string(str(i)) for i in values])
        sql = '''insert into %s (%s) values (%s)''' % (
            self.table, columns, values)
        sql = sql.replace('"None"', 'null').replace('""', 'null')
        return sql
