import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

class SitesSpider(CrawlSpider):
    name = "ucl-sites"
    allowed_domains = ['www.cs.ucl.ac.uk']
    start_urls = ['http://www.cs.ucl.ac.uk']
    rules = (
        Rule(SgmlLinkExtractor(allow=('www.cs.ucl.ac.uk',)) , callback='parse_items'),
    )

    def parse_items(self, response):
        extractor = LinkExtractor()
        links = extractor.extract_links(response)
        i = 0
        for link in links:
            if i > 5:
                break
            else:
                yield{ 
                'title': response.css("title").extract(),
                'url:' : link.url
                    }
                i = i + 1
    # def parse_items(self, response):
    #     hxs = HtmlXPathSelector(response)
    #     titles = hxs.xpath('//span[@class="pl"]')
    #     items = []
    #     for titles in titles:
    #         item = {}
    #         item["title"] = titles.xpath("a/text()").extract()
    #         item["link"] = titles.xpath("a/@href").extract()
    #         items.append(item)
    #     return items