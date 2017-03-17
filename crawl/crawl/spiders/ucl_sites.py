import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class SitesSpider(scrapy.Spider):
    name = "ucl-sites"
    allowed_domains = ['ucl.ac.uk']
    start_urls = ['http://ucl.ac.uk']
    rules = (
        Rule(SgmlLinkExtractor(allow=('.*ucl.ac.uk',)), follow=True),
        Rule(SgmlLinkExtractor(allow=('.*ucl.ac.uk',)), callback='parse'),
    )

    def start_requests(self):
        urls = [
            'http://ucl.ac.uk',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        extractor = LinkExtractor(allow_domains='ucl.ac.uk')
        links = extractor.extract_links(response)
        for link in links:
            yield{ 'url:' : link.url}