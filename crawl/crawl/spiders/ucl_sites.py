import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

import psycopg2
import sys

con = None

try:
     
    con = psycopg2.connect("dbname='search_engine_db' user='group27' host='searchengineindex.cwbjh0hhu9l3.us-west-2.rds.amazonaws.com' password='' port='5432'")   
    
    cur = con.cursor()

    cur.execute("CREATE TABLE Sites(Title VARCHAR(20), Link INT)")

    class SitesSpider(CrawlSpider):
        name = "ucl-sites"
        allowed_domains = ['www.cs.ucl.ac.uk']
        start_urls = ['http://www.cs.ucl.ac.uk']
        rules = (
            Rule(SgmlLinkExtractor(allow=('www.cs.ucl.ac.uk',)) , callback='parse_items', follow=True),
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
                    cur.execute("INSERT INTO Sites VALUES(titles.xpath("normalize-space(//title/text())").extract(),response.request.url)")
                    cur.execute("INSERT INTO Sites VALUES('Audi',52642)")
                    # yield{
                    #     'title' : titles.xpath("normalize-space(//title/text())").extract(),
                    #     'link' : response.request.url
                    # } 
                    i = i+1

except psycopg2.DatabaseError, e:

if con:
    con.rollback()

print 'Error %s' % e    
sys.exit(1)
    
    
finally:
    
    if con:
        con.close()