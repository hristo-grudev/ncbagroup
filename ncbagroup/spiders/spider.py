import scrapy

from scrapy.loader import ItemLoader

from ..items import NcbagroupItem
from itemloaders.processors import TakeFirst


class NcbagroupSpider(scrapy.Spider):
	name = 'ncbagroup'
	start_urls = ['https://ncbagroup.com/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="button__cta"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="title"]/text()').get()
		description = response.xpath('//div[@class="blog-detail-wrap"]/p//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="date"]/text()').get()

		item = ItemLoader(item=NcbagroupItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
