# quotes_scraper/spiders/quotes_spider.py

import scrapy
from ..items import MannanScrapyItem
class QuotesSpider(scrapy.Spider):
    name = "quotes"  
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        
        all_div_quotes = response.css('div.quote')
    
        items = QuoteItem()

        for quote_div in all_div_quotes:
            text = quote_div.css('span.text::text').extract_first()
            author = quote_div.css('.author::text').extract_first()
            tags = quote_div.css('.tag::text').extract()
            
            items['text'] = text
            items['author'] = author
            items['tags'] = tags

            yield items
        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            
            yield response.follow(next_page, callback=self.parse)        