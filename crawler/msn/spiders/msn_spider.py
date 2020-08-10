import scrapy
from urllib.parse import unquote
from ..items import NewsItem
import os
import json


class MSNSpider(scrapy.Spider):
    name = "msn"
    allowed_domains = ["msn.com"]

    # start_urls = []
    # with open(os.environ["MIND_NEWS_PATH"], 'r') as f:
    #     for l in f:
    #         _, _, _, _, _, url, _, _ = l.strip('\n').split('\t')
    #         start_urls.append(url)

    start_urls = [
        # ss
        "https://mind201910small.blob.core.windows.net/archive/AAGH0ET.html",
        # ar
        "https://mind201910small.blob.core.windows.net/archive/AABmf2I.html",
        # vi
        "https://mind201910small.blob.core.windows.net/archive/AAI33em.html"
    ]

    def __init__(self):
        with open('./doc_type.json', 'r') as f:
            self.doc_type = json.load(f)

        super().__init__()

    def parse(self, response):

        url = unquote(response.url)
        item = NewsItem()

        # parse nid, vert and subvert
        item['news_id'] = url.split('/')[-1].split('.')[-2]
        item['doc_type'] = self.doc_type[item['news_id']]

        # parse title from response
        item['title'] = response.xpath('//title//text()').getall()

        # parse body from response
        # type1: ar-nid
        if item['doc_type'] == 'ar':
            item['body'] = response.xpath('//p/text()').getall()

        # type2: ss
        if item['doc_type'] == 'ss':
            item['body'] = response.xpath('//div[@class="gallery-caption-text"]//text()').getall()

        # type3: vi
        if item['doc_type'] == 'vi':
            item['body'] = response.xpath('//div[@class="video-description"]//text()').getall()

        yield item
