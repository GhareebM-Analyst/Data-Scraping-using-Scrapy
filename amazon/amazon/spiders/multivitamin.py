import scrapy
from scrapy_splash import SplashRequest

class MultivitaminSpider(scrapy.Spider):
    name = 'multivitamin'
    def start_requests(self):
        url = 'https://www.amazon.com/s?k=multivitamin+for+kids'

        yield SplashRequest(url=url)

    def parse(self, response):
        products= response.css('div.a-section.a-spacing-small.puis-padding-left-small.puis-padding-right-small')
        for item in products:
            yield {
                'name' : item.css('span.a-size-base-plus.a-color-base.a-text-normal::text').get(),
                'price' : item.css('.a-price-whole::text').get(),
                'unit_price': item.css('.a-text-normal .a-color-secondary::text').get(),
                'count' : item.css('span.a-size-base.a-color-information.a-text-bold::text').get(),
                'link' : item.css('a').attrib['href']
            }

            next_page = response.css('.s-pagination-strip a').attrib['href']
            if response.css('span.s-pagination-item.s-pagination-next.s-pagination-disabled::text').get() is None:

                yield scrapy.Request(next_page,callback=self.parse)