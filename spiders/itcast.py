from scrapy import Request
from ..items import *
import random
import json
import re
from datetime import datetime

class NewsinaSpiderSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['sports.sina.com.cn']
    start_urls  = ['https://interface.sina.cn/pc_api/public_news_data.d.json?cre=tianyi&mod=nt_home_sports_global&merge=3&statics=1&tm=1601462230&offset=0&action=1&up=0&down=0&cids=57307&pdps=&top_id=&smartFlow=&editLevel=0,%201,%202,%203,%204&pageSize=50&type=sports_news,%20sports_slide']
    def parse(self, response):
        result = json.loads(response.text)
        data_list = result.get('data')
        for data in data_list:
            item = ItcastItem()

            ctime = datetime.fromtimestamp(int(data.get('ctime')))
            ctime = datetime.strftime(ctime, '%Y-%m-%d %H:%M')

            item['title'] = data.get('title')
            item['ctime'] = ctime
            item['url'] = data.get('url')
            yield Request(url=item['url'], callback=self.parse_content, meta={'item': item})

    # 进入到详情页面 爬取新闻内容
    def parse_content(self, response):
        item =response.meta['item']
        content = ''.join(response.xpath('//*[@id="artibody" or @id="article"]//p/text()').extract())
        img = response.xpath('//*[@id="artibody" or @id="article"]//div[@class="img_wrapper"]//img/@src').extract()
        keywords = response.xpath('//*[@id="keywords"]//a/text()').extract()
        content = re.sub(r'\u3000', '', content)
        content = re.sub(r'[ \xa0?]+', ' ', content)
        content = re.sub(r'\s*\n\s*', '\n', content)
        content = re.sub(r'\s*(\s)', r'\1', content)
        content = ''.join([x.strip() for x in content])
        item['keywords'] = keywords
        item['content'] = content[3::]
        item['img'] = img
        yield item
