import scrapy
from ..items import MannanScrapyItem

class Mannan(scrapy.Spider):
    name = "books"
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
       
        books = response.css('article.product_pod')

        for book in books:
            item = MannanScrapyItem()
            item['title'] = book.css('h3 a::attr(title)').get()
            item['price'] = book.css('p.price_color::text').get()
            item['availability'] = book.css('p.instock.availability::text').re_first('\S+')
           
            classes = book.css('p.star-rating').attrib.get('class')
            if classes:

                rating = classes.replace('star-rating', '').strip()
                item['rating'] = rating
            else:
                item['rating'] = None
            item['product_page'] = book.css('h3 a::attr(href)').get()
            
            item['product_page'] = response.urljoin(item['product_page'])

            yield item

        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)