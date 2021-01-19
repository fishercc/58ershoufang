import requests
import time
import re
from lxml import etree
from urllib import parse

if __name__ == "__main__":
    # 列表 存所有房源信息
    all_list = []
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "referer": "https://callback.58.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "cookie": "f=n; userid360_xml=71AA4CEB68A4149CDA14A2A28361DF12; time_create=1613562377170; commontopbar_new_city_info=1039%7C%E6%A1%82%E6%9E%97%7Cgl; commontopbar_ipcity=gl%7C%E6%A1%82%E6%9E%97%7C0; 58home=gl; f=n; id58=c5/nfGAFdP1IXzr8BJLkAg==; city=gl; 58tj_uuid=e545b9d1-11bb-4eae-ba4f-08ed2b4e949f; als=0; wmda_uuid=0278ee87d687e0add91317d28f20f11e; wmda_new_uuid=1; wmda_visited_projects=%3B6333604277682%3B11187958619315; xxzl_deviceid=qQzkzbOJK%2FfZfLdxTidwCiUFsRYbhqaHRcRz3w3vSb8WgkiGqRfUpFGmOh0%2FsWP2; new_uv=3; utm_source=; spm=; init_refer=https%253A%252F%252Fgl.58.com%252F; JSESSIONID=EE94A4B17DF46A65C22A06121B59E493; wmda_session_id_6333604277682=1611020022213-0c3f26c0-70fb-ca44; new_session=0; wmda_session_id_11187958619315=1611020026684-ada47e50-82fd-ea6f; xzfzqtoken=4G0WPQRyevcLytlmNCJccPCJKF%2F3NJA5yz8iyE%2Fw%2FSmm09xD9TFbpGknRTOBr4rUin35brBb%2F%2FeSODvMgkQULA%3D%3D",
    }
    keyword = input('请输入关键词(默认悉尼蓝湾，直接回车):')
    if keyword == '':
        keyword ='悉尼蓝湾'
    url = 'https://gl.58.com/ershoufang/?key={}'.format(parse.quote(keyword))
    page_text = requests.get(url=url, headers=headers).text
    #获取最大页码
    tree = etree.HTML(page_text)
    page_sum = 1
    try:
        a_list = tree.xpath('//div[@class="pager"]/a')
        page_sum_str = a_list[-2].xpath('./span/text()')[0]
        if page_sum_str!=None:
            page_sum = int(page_sum_str)
    except:
        page_sum = 1


    for page in range(page_sum):

        if (page+1)>1:
            url = 'https://gl.58.com/ershoufang/pn{}/?key={}'.format(page+1,parse.quote(keyword))
            page_text = requests.get(url=url, headers=headers).text

        tree = etree.HTML(page_text)
        li_list = tree.xpath('//ul[@class="house-list-wrap"]/li')
        for li in li_list:
            temp_list = li.xpath('./div[2]/h2/a//text()')
            base_info1 = li.xpath('./div[2]/p/span[1]/text()')[0]
            base_info2 = li.xpath('./div[2]/p/span[2]/text()')[0]
            base_info = base_info1+','+base_info2
            #总价
            price_sum = li.xpath('./div[3]/p[1]/b/text()')[0]
            #每平多少元
            price_uint_str =li.xpath('./div[3]/p[2]/text()')[0]
            title = ''
            for e in temp_list:
                title = title+e

            content = title+'('+base_info+')['+price_sum+'万,'+price_uint_str+']'
            print(content)
            ex = '(\d{4,})'
            t4 = re.findall(ex,price_uint_str,re.S)
            price_uint= int(t4[0])
            #print(price_uint)
            #去除空格
            content = "".join(content.split())
            #构造字典
            one_dict = {
                'title':content,
                'price_sum':price_sum,
                'price_uint':price_uint,
            }
            all_list.append(one_dict)
        time.sleep(3)



    #统计数据
    #计算平均值
    sum = 0
    for l in all_list:
        sum = sum + l['price_uint']
    sum_size =len(all_list)
    avg = 0
    if sum_size!=0:
        avg = sum // sum_size
        result_list = sorted(all_list,key=lambda x: (x['price_uint']))
        avg_str = '平均单价：{}/㎡ ，最高单价：{}/㎡,最低单价：{}/㎡,107㎡建议售价：{}万,收集58同城{}个数据\n\n'.format(avg,result_list[-1]['price_uint'],result_list[0]['price_uint'],avg*107//10000,len(result_list))
        filename = './{}_58.txt'.format(keyword)
        fp = open(filename, 'w', encoding='utf-8')
        fp.write(avg_str)
        count = 0
        for l in result_list:
            count = count+1
            str = '{}、'.format(count)+l['title']
            fp.write( str)
            fp.write('\n')
        fp.close()

    else:
        print('你被限制访问了，请用浏览器手动验证')
