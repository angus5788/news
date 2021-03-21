# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ItcastItem(scrapy.Item):
   ctime = scrapy.Field()  # 发布时间
   url = scrapy.Field()
   title = scrapy.Field()  # 新闻标题
   keywords = scrapy.Field()  # 关键词
   content = scrapy.Field()  # 新闻内容
   img = scrapy.Field()

