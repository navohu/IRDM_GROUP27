from scrapy.item import Item, Field

class SitegraphItem(Item):
     url=Field()
     linkedurls=Field()