import matplotlib.pyplot as plt
import numpy as np
from MySqlHeper import MysqlHelper
import matplotlib.ticker as mtick


#访问数据库
keyword='悉尼蓝湾'
MySql = MysqlHelper(user='root', pwd='123456', port=3306, host='127.0.0.1', db_name='my58')
sql ="SELECT AVG(priceUint) AS avgprice,createtime,COUNT(keyword) AS num FROM xinilanwan WHERE keyword='{}' GROUP BY createtime ORDER BY createtime;".format(keyword)
QueryRes = MySql.select(sql=sql)
all_list = QueryRes['result']
num = QueryRes['effect']
if num>1 :
    avg_price_list = []
    create_time_list = []
    count_list = []
    for l in all_list:
        avg_price = int(l['avgprice'])
        dtime = l['createtime']
        count = l['num']
        create_time = dtime.strftime('%m-%d')
        avg_price_list.append(avg_price)
        create_time_list.append(create_time)
        count_list.append(count)
    x = np.array(create_time_list)
    y = np.array(avg_price_list)

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
    fig, ax1 = plt.subplots()
    plt.title(keyword+'二手房价趋势图')
    #均价图
    ax1.plot(x, y, 'o-',color='red', label='均价')
    ax1.set_xticks(x)
    ax1.set_xticklabels(create_time_list)
    ax1.set_xlabel(u"日期")
    ax1.set_ylabel(u"元/㎡")
    max_score = max(avg_price_list)
    ax1.set_ylim(0, int(max_score * 1.2))
    # 变化率标签
    for xx, yy in zip(x, avg_price_list):
        ax1.text(xx, yy + max_score * 0.02, ('%d' % yy), ha='center', va='bottom', fontsize=13)

    #数量图
    ax2 = ax1.twinx()
    y = np.array(count_list)
    ax2.plot(x, y, 'o-',color='blue', label='套数')
    max_proges = max(count_list)
    # 变化率标签
    for xx, yy in zip(x, count_list):
        ax2.text(xx, yy + max_proges * 0.02, ('%d' % yy), ha='center', va='bottom', fontsize=13)
    # 设置纵轴格式
    fmt = '%d'
    yticks = mtick.FormatStrFormatter(fmt)
    ax2.yaxis.set_major_formatter(yticks)
    ax2.set_ylim(0, int(max_proges * 1.5))
    ax2.set_ylabel('套数')

    # 图例
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    plt.legend(handles1 + handles2, labels1 + labels2, loc='upper right')
    plt.show()
else:
    print("只有1个数据记录！")
