import scrapy
import re
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

class SitesSpider(CrawlSpider):
    name = "ucl-sites"
    allowed_domains = ['ucl.ac.uk']
    with open("../src/subdomains.txt", "rt") as f:
        start_urls = [url.strip() for url in f.readlines()]
    rules = (
        Rule(SgmlLinkExtractor(allow=(r'.*.ucl.ac.uk',), deny=("metalib.ucl.ac.uk"),) , callback='parse_items', follow=True),
    )
    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.xpath('//div')
        items = []
        i = 0
        for titles in titles:
            if i > 0:
                break
            else:
                yield{
                    'title' : titles.xpath("normalize-space(//title/text())").extract(),
                    'link' : response.request.url
                } 
                i = i+1