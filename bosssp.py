import scrapy


class BossspSpider(scrapy.Spider):
    name = 'bosssp'
    allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.zhipin.com/c101280600-p100102/?page={}&ka=page-{}']

    def parse(self, response):
        pass
