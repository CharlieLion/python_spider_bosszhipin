from scrapy.utils.trackref import print_live_refs
from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from lxml import etree

edge_options = EdgeOptions()
edge_options.use_chromium = True
# 设置无界面模式，也可以添加其它设置
# edge_options.add_argument('headless')
driver = Edge(options=edge_options)
driver.get('https://www.163.com/news/article/GG0MUGTK00018AP2.html')
content = driver.page_source


content = etree.HTML(content)
li_list = content.xpath('//*[@id="content"]/div[2]/p/text()')
context = ''.join(li_list)
print(li_list)
print(context)
# for item in li_list:
#     title = item.xpath('./div/h3/a.text').extract()[0]
#     print(title)

driver.quit()