from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from qna.items import qnaItem

# For converting the unicode data to the normal string
import unicodedata

class qnaSpider(CrawlSpider):
    name = 'qnaCrawl'
    allowed_domains = ['amazon.in']
    start_urls = ['http://www.amazon.in/Chevron-Motorola-Rubberised-Matte-Cover/dp/B01LI6QOX6/ref=pd_sim_107_1?ie=UTF8&psc=1&refRID=0TFS22D7Y9BNDP69SH60']
    rules = (Rule(LinkExtractor(), callback='parse', follow=True),)
    

    def parse(self, response):

        #print response.body

        #Name of the product
        productName = ''.join(response.xpath('//*[@id="productTitle"]/text()').extract()[:])
        print '________________________________________________________________________________________________________________________________________'
        print "Name of the product : ",
        print unicodedata.normalize('NFKD', productName).encode('ascii','ignore').replace('\n', '').strip()

        # Prize of the product
        productPrice = ''.join(response.xpath('//*[@id="priceblock_saleprice"]/text()').extract()[:])
        print "Price : ",
        print unicodedata.normalize('NFKD', productPrice).encode('ascii','ignore').replace('\n', '').strip()
        print '________________________________________________________________________________________________________________________________________'

        # Links in the reponse
        links = response.xpath('//ul/li/a/@href').extract()
        items = qnaItem()

        for link in links:
            items['link'] = link

        return items