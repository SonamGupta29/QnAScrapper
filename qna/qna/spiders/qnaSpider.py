from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from qna.items import qnaItem

# For converting the unicode data to the normal string
import unicodedata


class qnaSpider(CrawlSpider):
    name = 'qnaCrawl'
    allowed_domains = ['amazon.in']
    start_urls = ['http://www.amazon.in/gp/product/B00UTKPKHY/ref=s9_acsd_al_bw_c_x_1?pf_rd_m=A1VBAL9TL5WCBF&pf_rd_s=merchandised-search-1&pf_rd_r=0Q5X4CR78HVCMVGVE9GW&pf_rd_t=101&pf_rd_p=999044747&pf_rd_i=4363185031']
    #rules = (Rule(SgmlLinkExtractor(allow=(r'amazon\.in'), deny = (r'\/help\/', 
      #                                              r'\/product\-reviews\/')), callback='parse_links'),)
    rules = (Rule(LinkExtractor(), callback='parse_links'),)

    def parse_links(self, response):

        #print response.body

        f = open("productDB", "a")

        #f.write(response.body)

        #Name of the product
        productName = ''.join(response.xpath('//*[@id="productTitle"]/text()').extract())
        print '________________________________________________________________________________________________________________________________________'
        print "Name of the product : ",

        # Check if the string is unicode or not
        if isinstance(productName, unicode):
            productName = unicodedata.normalize('NFKD', productName).encode('ascii','ignore').replace('\n', '').strip()
        else:
            productName = productName.replace('\n', '').strip()
        print productName
        f.write(productName)

        # Prize of the product
        productPrice = ''.join(response.xpath('//*[@id="priceblock_ourprice"]/text()').extract())
        print "Price : ",

        # Check if the string is unicode or not
        if isinstance(productPrice, unicode):
            productPrice = unicodedata.normalize('NFKD', productPrice).encode('ascii','ignore').replace('\n', '').strip()
        else:
            productPrice = productPrice.replace('\n', '').strip()
        print productPrice
        f.write('\n' + productPrice)
        print '________________________________________________________________________________________________________________________________________'

        # Links in the reponse        
        links = response.xpath('//@href').extract()
        items = []
        for link in links:
            item = qnaItem()

            # Check if the link is unicode or not
            if isinstance(link, unicode):
                link = unicodedata.normalize('NFKD', link).encode('ascii','ignore').replace('\n', '').strip()
            else:
                link = link.replace('\n', '').strip()

            # Check if the string starts using amazon.com if not append it or simply we can check if start contains /

            if len(link) > 4 and link[0] == '/':
                link = 'http://amazon.in' + link

            item['links'] = link
            items.append(item)
        
        f.close()

        return items