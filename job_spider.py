# -*- coding: utf-8 -*-                                                                                                                                                                         #关注微信公众号“和你学Python”可获取更多资源

#导入requests库
import requests

#导入re模块
import re

#从bs4导入BeautifulSoup
from bs4 import BeautifulSoup

#已获取的地区代码
area_code = {'北京': '010000', '上海': '020000', '广州': '030200', '深圳': '040000', '武汉': '180200', '西安': '200200', '杭州': '080200', '南京': '070200', '成都': '090200', '重庆': '060000', '东莞': '030800', '大连': '230300', '沈阳': '230200', '苏州': '070300', '昆明': '250200', '长沙': '190200', '合肥': '150200', '宁波': '080300', '郑州': '170200', '天津': '050000', '青岛': '120300', '济南': '120200', '哈尔滨': '220200', '长春': '240200', '福州': '110200', '珠三角': '01'}

#网页的链接，关键词位置用{}代替，留待格式化
url = 'https://search.51job.com/list/{}000000,0000,00,9,99,{}2,{}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

#定义最大页面数
MAX_PAGE = 10

#定义需要爬取的地区列表，列表里可以有多个地区
area_list = ['北京', '上海']

#定义职位名
position = '会计'

#定义获取的数据列表
datas = []

#获取所有的职位链接
def get_url():
    #若地区为1个，直接作为参数
    if len(area_list) == area_list:
        final_area = area_code[area_list[0]]
    #若地区大于1个，把地区代码用%252C拼接起来
    else:
        final_area = '%252C'.join([area_code[area] for area in area_list])

    #定义存放职位链接的列表
    url_list = []

    #根据最大页面值的次数
    for page in range(1, MAX_PAGE+1):
        #请求网页并把响应体赋值给response
        response = requests.get(url.format(final_area + ',', position + ',', page))

        #将页面编码改为gbk
        response.encoding = 'gbk'

        #获取所有的a节点
        bs = BeautifulSoup(response.text, 'lxml').find_all('a', target='_blank')

        #获取所有职位链接并加入到url_list
        for a in bs:
            if a.get('href')[-14:] == '.html?s=01&t=0':
                url_list.append(a.get('href'))

    #返回获取了所有url的列表
    return url_list

#定义获取数据的函数
def get_data(url):
    #定义一个保存数据的列表
    lst = []
    
    #获取页面html
    response = requests.get(url)

    #将页面编码改为gbk
    response.encoding = 'gbk'

    #获取公司名
    lst.append(re.search('class="catn">(.*?)<em', response.text, re.S).group(1))
    
    #把链接也保存下来
    lst.append(url)

    #获取包含工资和职位名的字符串
    whole = re.search('<h1 title="(.*?)">.*?</h1><strong>(.*?)</strong>', response.text, re.S)

    #获取职位名
    lst.append(whole.group(1))

    #获取工资
    lst.append(whole.group(2))

    #获取div里的内容
    p_list = re.findall('<div class="bmsg job_msg inbox">(.*?)<div class="mt10">', response.text, re.S)

    #获取所有p标签里的内容
    jd_list = re.findall('>(.*?)<', p_list[0], re.S)

    #定义职位描述字符串
    job_description = ''

    #把所有p标签的内容拼接在一起
    for jd in jd_list:
        job_description += jd

    #去除多余的空格和字符
    if (re.sub('\s|(&.*?;)', '', job_description)):
        lst.append(re.sub('\s|(&.*?;)', '', job_description))
    else:
        lst.append(re.sub('\s|(&.*?;)', '', p_list[0]))

    #把保存了数据的列表加入数据列表
    datas.append(lst)

    print('已获取' + whole.group(1) + '职位的数据')

#定义保存文件的函数
def save(lst):
    #定义将要写入的字符串
    data_str = ''

    #遍历所有数据并用逗号连接起来
    for data in datas:
        data_str = data_str + ','.join(data) + '\n'

    #保存为文件
    with open(r'C:\Users\Administrator\Desktop\data.csv', 'w', encoding='utf-8') as f:
        f.write('\ufeff')
        f.write(data_str)

if __name__ == '__main__':
    print('前程无忧爬虫开始启动')
    
    #获取页面列表并赋值到url_list
    url_list = get_url()

    #遍历url_list里的url去获取数据
    for url in url_list:
        get_data(url)

    #把数据保存为文件
    save(datas)

    print('文件已保存')
