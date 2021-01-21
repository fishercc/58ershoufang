import pymysql


class MysqlHelper:
    def __init__(self, user, pwd, port, host, db_name):
        self._user = user
        self._password = pwd
        self._charset = 'utf8'
        self._port = port
        self._host = host
        self._db_name = db_name
        self._conn = self.connect_mysql()
        if self._conn:
            self._cursor = self._conn.cursor()

    def connect_mysql(self):
        """
        连接数据库
        :return:
        """
        conn = pymysql.connect(host=self._host,
                               user=self._user,
                               passwd=self._password,
                               db=self._db_name,
                               port=self._port,
                               cursorclass=pymysql.cursors.DictCursor,
                               charset=self._charset,
                               use_unicode=True,
                               )
        return conn

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        self._cursor.close()
        self._conn.close()

    def execute(self, *args, params=None):
        """
        执行多条sql
        :param params:
        :param args:
        :return:
        """
        if params is None:
            params = []
        effect = 0
        try:
            for sql in args:
                num = self._cursor.execute(sql, params)
                effect += num
            self._conn.commit()
        except Exception as e:
            # 发生错误时回滚
            self._conn.rollback()
            print(e)
        self.close()
        return effect

    def select_multi(self, *args, params=None):
        """
        查询语句，可以执行多条查询
        :param args:
        :param params:
        :return: 返回元祖res：结果，num查询出行数
        """
        if params is None:
            params = []
        i = 1
        res = {}
        for sql in args:
            num = self._cursor.execute(sql, params)
            sql_results = self._cursor.fetchall()
            res['result%s' % i] = sql_results
            res['effect%s' % i] = num
            i += 1
        self.close()
        return res

    def select(self, sql, act='all'):
        """
        查询语句方法
        :param act:
        :param sql:
        :return: 返回字典res：结果，num查询出行数
        """
        global res
        if act == 'all':
            num = self._cursor.execute(sql)
            sql_results = self._cursor.fetchall()
            res = {
                'result': sql_results,
                'effect': num
            }
        self.close()
        return res
