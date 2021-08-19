from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
import re
from lxml import etree
import time
import numpy as np
import csv
import xlwt

info_list = []

def select_agent():
    """
    随机返回一个agent 防止反扒
    @return: headers
    """

    user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
     ]
    headers = {'User-Agent': np.random.choice(user_agent_list)}
    return headers

def saveData(datalist,savepath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0) # 创建workbook对象
    sheet = book.add_sheet('page1', cell_overwrite_ok=True) # 创建工作表
    for i in range(len(datalist)):
        data = datalist[i]
        for j in range(len(data)):
            sheet.write(i,j,data[j])  # 数据
    book.save(savepath) # 保存
    print('保存成功！')

def init():

    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument('headless')
    driver = Edge(options=edge_options) #(capabilities=EDGE) executable_path='msedgedriver.exe'
    return driver

def spider(i):
    driver = init()
    print('第{}页'.format(i))
    driver.get('https://www.zhipin.com/c101280600-p100109/?page={}&ka=page-{}'.format(i, i))
    page_text = driver.page_source
    tree = etree.HTML(page_text)
    list = tree.xpath('//div[@class="job-list"]/ul/li')
    if list ==[]:
        return -1
    for item in list:
        name = item.xpath('.//span[@class = "job-name"]/a/text()')[0]
        loc = item.xpath('.//span[@class="job-area"]/text()')[0]
        salary = item.xpath('.//div[@class="job-limit clearfix"][1]/span/text()')[0]
        yearLimit = item.xpath('.//div[@class="job-limit clearfix"]/p/text()')[0]
        degree = item.xpath('.//div[@class="job-limit clearfix"]/p/text()')[1]
        company = item.xpath('.//div[@class="company-text"]/h3/a/text()')[0]
        company_detail_first = item.xpath('.//div[@class="company-text"]/p/a/text()')[0]
        company_detail = ', '.join(item.xpath('.//div[@class="company-text"]/p/text()'))
        tag = ', '.join(item.xpath('.//div[@class="tags"]/span/text()'))
        ip_address ='https://www.zhipin.com'+item.xpath('.//div[@class="primary-wrapper"]/div/@href')[0]
        info_list.append((name, loc, salary, yearLimit, degree, company, company_detail_first, company_detail, tag, ip_address))

    time.sleep(1)
    driver.close()
    return 1
if __name__ == '__main__':
    # start_time = time.time()
    for i in range(1,50):

        try:
            utag = spider(i)
        except Exception as ex:
            print(ex)
        if(utag==-1):
            break

    saveData(info_list, 'boss_python.xls')

