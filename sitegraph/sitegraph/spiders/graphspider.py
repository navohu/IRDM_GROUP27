from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.utils.url import urljoin_rfc
from sitegraph.items import SitegraphItem
import psycopg2


def fetch_urls():
    urls = []
    try:
     
        con = psycopg2.connect("dbname='search_engine_db' user='group27' password='' host='searchengineindex.cwbjh0hhu9l3.us-west-2.rds.amazonaws.com' port='5432'")   
        cur = con.cursor()
        query = "SELECT link FROM `cs_sites`"
        cur.execute(query)
        for i,row in list(cur.fetchall()):
            urls.append(row[i])
        con.commit()

    except psycopg2.DatabaseError, e:
        
        if con:
            con.rollback()
        
        print 'Error %s' % e    
        sys.exit(1)

    return urls

    

for i,row in enumerate(cursor.fetchall()):
   options.append(row[i])

class GraphspiderSpider(CrawlSpider):
    name = 'graphspider'
    start_urls = fetch_urls()

    rules = (
        Rule(SgmlLinkExtractor(), callback='parse_item'),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        urlname = response.url
        item = SitegraphItem()
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