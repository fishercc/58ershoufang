import requests
import time
import re
from lxml import etree
from urllib import parse
from SaveToDB import  SaveTool
import datetime
import sys


def realTimeGet():
    keyword = input('请输入关键词(默认悉尼蓝湾，直接回车):')
    if keyword == '':
        keyword = '悉尼蓝湾'
    # 列表 存所有房源信息
    all_list = []
    headers = {
        "host": "gl.58.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "cookie": "userid360_xml=71AA4CEB68A4149CDA14A2A28361DF12; time_create=1613562377170; f=n; commontopbar_new_city_info=1039%7C%E6%A1%82%E6%9E%97%7Cgl; 58home=gl; id58=c5/nfGAFdP1IXzr8BJLkAg==; city=gl; 58tj_uuid=e545b9d1-11bb-4eae-ba4f-08ed2b4e949f; als=0; wmda_uuid=0278ee87d687e0add91317d28f20f11e; wmda_new_uuid=1; wmda_visited_projects=%3B6333604277682%3B11187958619315; xxzl_deviceid=qQzkzbOJK%2FfZfLdxTidwCiUFsRYbhqaHRcRz3w3vSb8WgkiGqRfUpFGmOh0%2FsWP2; sessid=5FBF9842-2C06-45F5-B8EE-714DF935BA19; aQQ_ajkguid=84A89C36-4D1E-4003-8CC4-E15E0113819A; wmda_visited_projects=%3B6333604277682%3B11187958619315%3B8788302075828; ctid=1039; cid=1039; myfeet_tooltip=end; f=n; commontopbar_new_city_info=1039%7C%E6%A1%82%E6%9E%97%7Cgl; commontopbar_ipcity=nn%7C%E5%8D%97%E5%AE%81%7C0; new_uv=13; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253Ds9mZP0PgGyMy8WyhESC6YpXldaqNxrDHx7daxHCUoDi%2526wd%253D%2526eqid%253Db0260653000330dc00000006600fe34d; wmda_session_id_11187958619315=1611653974933-b7a64728-c475-8291; xxzl_cid=014738718b78413190e537639b0bdfe6; xzuid=2bb08420-5beb-44ba-9f9f-01188674cf79; new_session=0",
    }
    url = 'https://gl.58.com/ershoufang/?key={}'.format(parse.quote(keyword))
    page_text = requests.get(url=url, headers=headers).text
    #获取最大页码
    tree = etree.HTML(page_text)
    page_sum = 1
    try:
        a_list = tree.xpath('//li[@class="page-item last"]')
        page_sum_str = a_list[0].xpath('./a/text()')[0]
        if page_sum_str!=None:
            page_sum = int(page_sum_str)
    except:
        page_sum = 1


    for page in range(page_sum):

        if (page+1)>1:
            url = 'https://gl.58.com/ershoufang/pn{}/?key={}'.format(page+1,parse.quote(keyword))
            page_text = requests.get(url=url, headers=headers).text

        tree = etree.HTML(page_text)
        li_list = tree.xpath('//div[@class="property"]')
        for li in li_list:
            #标题
            temp_list = li.xpath('./a/div[2]/div[1]/div[1]/h3//text()')
            #几房
            base_info1 = ''.join(li.xpath('./a//p[@class="property-content-info-text property-content-info-attribute"]//text()'))
            # 去除空格
            base_info1 = "".join(base_info1.split())
            base_info2 = li.xpath('./a//div[@class="property-content-info"]/p[2]/text()')[0]
            base_info = base_info1+','+base_info2
            #总价
            price_sum = li.xpath('./a//span[@class="property-price-total-num"]/text()')[0]
            price_sum="".join(price_sum.split())
            #每平多少元
            price_uint_str =li.xpath('./a//p[@class="property-price-average"]/text()')[0]
            title = ''
            for e in temp_list:
                title = title+e

            content = title+'('+base_info+')['+price_sum+'万,'+price_uint_str+']'
            ex = '(\d{4,})'
            t4 = re.findall(ex,price_uint_str,re.S)
            price_uint= int(t4[0])
            #print(price_uint)
            #去除空格
            content = "".join(content.split())
            print(content)
            #构造字典
            one_dict = {
                'title':content,
                'price_sum':price_sum,
                'price_uint':price_uint,
            }
            all_list.append(one_dict)
        time.sleep(3)

    if len(all_list) >0:
        '''#去重
        news_all_list = []
        for id in all_list:
            if id not in news_all_list:
                news_all_list.append(id)
        '''
        #排序
        result_list = sorted(all_list,key=lambda x: (x['price_uint']))

        #保存到数据库
        st = SaveTool()
        st.savetodb(result_list,keyword=keyword)
        #保存到文件----------------------
        dt = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = '{}_58({}).txt'.format(keyword,dt)
        st.savetofile(filename=filename,result_list=result_list)
    else:
        print('你被限制访问了，请用浏览器手动验证')


if __name__ == "__main__":
    choice_function  = input('请选择功能：\n1：查询当天数据\n2：从数据库中查询指定日期数据\n')
    if choice_function == '1':
        realTimeGet()
    elif choice_function == '2':
        keyword = input('请输入关键字:')
        querydate = input('请输入查询的日期(格式：2021-01-20):')
        if keyword == '':
            keyword = '悉尼蓝湾'
        if querydate == '':
            querydate = '2021-01-20'
        st = SaveTool()
        st.savetofilefromdb(QueryTime=querydate, keyword=keyword)
    else:
        print('没有此功能')
        sys.exit(1)