import scrapy
from ..items import AmazonItem

#https://stackoverflow.com/questions/4998427/how-to-group-elements-in-python-by-n-elements
def grouper(N, iterable, fillvalue=None):
	hardcover_prices = []
	subList = [iterable[n:n+N] for n in range(0, len(iterable), N)]
	for value in subList:
		hardcover_prices.append(''.join(map(str,value)))
	return hardcover_prices

class AmazonSpider(scrapy.Spider):
	name = 'amazonbot'

	page_number = 2

	start_urls = ['https://www.amazon.com/s?k=keyboard&rh=n%3A468642&dc&qid=1590803910&rnid=2941120011&ref=sr_nr_n_5']


	def parse(self, response):
		items = AmazonItem()

		#Try function with different possible css classes. ##############
		title = response.css('.a-color-base.a-text-normal::text').extract() 
		hardcover_price = response.css('.a-price span span::text').extract()
		reviews = response.css('.a-size-small .a-link-normal .a-size-base::text').extract()
		#audible_price = response.css('.a-spacing-top-small .a-price span span::text').extract()
		hardcover_prices = grouper(4,hardcover_price)

		items['title'] = title
		items['price'] = hardcover_prices
		items['reviews'] = reviews
		yield items

		next_page = 'https://www.amazon.com/s?k=keyboard&i=videogames&rh=n%3A468642&dc&page={}&qid=1590805089&rnid=2941120011&ref=sr_pg_{}'.format(AmazonSpider.page_number,AmazonSpider.page_number-1)
		if AmazonSpider.page_number <= 399:
			AmazonSpider.page_number += 1
			yield response.follow(next_page, callback=self.parse)