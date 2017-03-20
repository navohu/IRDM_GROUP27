import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy import Selector

class SitesSpider(CrawlSpider):
    name = "content"
    f = open("url.txt")
    start_urls = [url.strip() for url in f.readlines()]
    f.close()
    rules = (
        Rule(SgmlLinkExtractor() , callback='read_content'),
    )
    def parse_items(self, response):
        sel = Selector(response)
        text = ''.join(sel.select("//body//text()").extract()).strip().replace("\r","").replace("\n","").replace("\t","")
        print("TEXT ------ " + text)
        i = 0
        for content in text:
            if i > 0:
                break
            else:
                yield{
                    'link' : response.request.url,
                    'content': text
                } 
                i = i+1