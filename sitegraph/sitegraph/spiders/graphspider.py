from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.utils.url import urljoin_rfc
from sitegraph.items import SitegraphItem

class GraphspiderSpider(CrawlSpider):
    name = 'graphspider'
    allowed_domains = ['www.cs.ucl.ac.uk']
    start_urls = ['http://www.cs.ucl.ac.uk']

    rules = (
        Rule(SgmlLinkExtractor(allow='www.cs.ucl.ac.uk'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        urlname = response.url
        item = SitegraphItem()
        # item['url'] = response.url
        llinks=[]
        i = 0
        for anchor in hxs.select('//a[@href]'):
            href=anchor.select('@href').extract()[0]

            if not href.lower().startswith("javascript"):
                llinks.append(urljoin_rfc(response.url,href))
                json = {urlname: llinks}
                item['url'] = json
            i = i+1
        return item