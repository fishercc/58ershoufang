from MySqlHeper import MysqlHelper
import datetime


class SaveTool:
    def __init__(self):

        '''
        sql = "INSERT INTO xinilanwan(title, priceSum, priceUint,time) VALUES ('标题1', 65, 5000,'2021/01/20 10:49:20');"
        res = MySql.execute(sql,params=None)
        if res == 1:
            print('sql执行成功\n')
        '''

    def savetodb(self, data_list, keyword):
        dt = datetime.datetime.now().strftime("%Y-%m-%d")
        self.queryanddel(QueryTime=dt,keyword=keyword)
        MySql = MysqlHelper(user='root', pwd='123456', port=3306, host='127.0.0.1', db_name='my58')
        all_sql = []
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for li in data_list:
            sql = "INSERT INTO xinilanwan(title, priceSum, priceUint,createtime,keyword) VALUES ('{}', {}, {},'{}','{}');".\
                format(li['title'],li['price_sum'],li['price_uint'],dt,keyword)
            all_sql.append(sql)

        res = MySql.execute(*all_sql, params=None)
        if res <= 0:
            print('sql执行成功失败\n')
        else:
            print('成功保存{}条数据到数据库！\n'.format(res))
    def savetofile(self,filename,result_list):
        # 统计数据
        # 计算平均值
        sum = 0
        for l in result_list:
            sum = sum + l['price_uint']
        sum_size = len(result_list)
        avg = 0
        avg = sum // sum_size
        avg_str = '平均单价：{}/㎡ ，最高单价：{}/㎡,最低单价：{}/㎡,107㎡建议售价：{}万,收集58同城{}个数据\n\n'. \
        format(avg, result_list[-1]['price_uint'], result_list[0]['price_uint'], avg * 107 // 10000,
               len(result_list))
        fp = open(filename, 'w', encoding='utf-8')
        fp.write(avg_str)
        count = 0
        for l in result_list:
            count = count + 1
            str = '{}、'.format(count) + l['title']
            fp.write(str)
            fp.write('\n')
        fp.close()
        print('\n'+filename + '保存成功！')

        #从数据库中读取数据并保存到文件中
    def savetofilefromdb(self,QueryTime='2021-01-20',keyword='悉尼蓝湾'):
        all_list = []
        title = ''
        price_sum = 50
        price_uint = 5000
        #访问数据库
        MySql = MysqlHelper(user='root', pwd='123456', port=3306, host='127.0.0.1', db_name='my58')
        sql ="SELECT title,priceSum AS price_sum,priceUint AS price_uint FROM xinilanwan WHERE DATE_FORMAT(createtime,'%Y-%m-%d')='{}' AND keyword='{}';".\
                format(QueryTime,keyword)
        QueryRes = MySql.select(sql=sql)
        all_list = QueryRes['result']
        num = QueryRes['effect']
        if num <= 0:
            print('数据库无此结果')
        else:
            dt = QueryTime
            filename = '{}_58({}).txt'.format(keyword, dt)
            self.savetofile(filename=filename, result_list=all_list)

    def queryanddel(self, QueryTime = '2021-01-20', keyword = '悉尼蓝湾'):
        MySql = MysqlHelper(user='root', pwd='123456', port=3306, host='127.0.0.1', db_name='my58')
        sql = "SELECT title,priceSum AS price_sum,priceUint AS price_uint FROM xinilanwan WHERE DATE_FORMAT(createtime,'%Y-%m-%d')='{}' AND keyword='{}';". \
            format(QueryTime, keyword)
        QueryRes = MySql.select(sql=sql)
        num = QueryRes['effect']
        if num > 0:
            #执行删除操作
            MySql2 = MysqlHelper(user='root', pwd='123456', port=3306, host='127.0.0.1', db_name='my58')
            sql = "DELETE FROM xinilanwan WHERE DATE_FORMAT(createtime,%s)=%s AND keyword=%s;"
            res = MySql2.execute(sql, params=['%Y-%m-%d',QueryTime, keyword])
            if res <= 0:
                print('sql执行成功失败\n')
            else:
                print('数据库删除{}的{}条数据！\n'.format(QueryTime,res))




'''
#保存到数据库
st = SaveTool()
result_list = [
{'title':'标题1', 'price_sum':25, 'price_uint':5000},
{'title':'标题2', 'price_sum':35, 'price_uint':5000},
{'title':'标题3', 'price_sum':45, 'price_uint':5000},
               ]
st.savetodb(result_list)

st = SaveTool()
st.savetofilefromdb()
'''
