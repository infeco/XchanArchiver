# -*- coding: utf-8 -*-

from datetime import datetime as dt

from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import Rule, CrawlSpider

from ..items import FourchanItem


class FourchanSpiderSpider(CrawlSpider):
	name = 'fourchan_spider'
	allowed_domains = ['boards.4chan.org']
	start_urls = ['https://boards.4chan.org/pol/']

	# Initially extract all the links for all the posts and all pages where next posts are stored
	# e.g boards.4chan.org/pol/2/, boards.4chan.org/pol/3/ so on

	rules = (
		Rule(
			LinkExtractor(
				restrict_xpaths='//div[@class="mPagelist mobile"]/div[@class="next"]/a/@href',
			)
		),
		Rule(
			LinkExtractor(
				restrict_xpaths='//form[@id="delform"]/div[@class="board"]/div[@class="thread"]/div[1]/div['
								+ '@class="postLink mobile"]//a/@href',
				allow_domains=allowed_domains,
				unique=True
			),
			callback='post_scrape'
		)
	)

	def post_scrape(self, response):
		# Here we scrape the post from site
		item = FourchanItem()
		post = Selector(response.xpath('//form[@id="delform"]/div[@class="board"]/div[@class="thread"]'
											+ '/div[contains(@class," opContainer")]/div[startswith(@class,"post")]'))

		post_replies = Selector(response.xpath('//form[@id="delform"]/div[@class="board"]/div[@class="thread"]'
											+ '/div[contains(@class," replyContainer")]/div[startswith(@class,"post ")]'))

		post_info = post.xpath('.//div[startswith(@class,"postInfo ")]')

		thread_replies = response.xpath('//form[@id="delform"]/div[@class="board"]/div[@class="thread"]/'
												+ 'div[contains(@class,"replyContainer")]')

		item['post_scraped_time'] = dt.now().strftime('%m/%d/%Y')
		item['post_replies_count'] = post.xpath('.//div[@class="board"]/div[startswith(@class,"navLinks ")]/div[@class'
												+ '="thread-stats"]/span[@class="ts-replies"]/text()').extract_first()

		post_reply_ids = ''
		post_reply_contents = ''
		post_reply_user_ids = ''
		post_reply_timestamps = ''

		item['post_replies'] = ''
		# Post_Replies = [ {'reply_user_id', 'reply_content', 'reply_timestamp', 'reply_id'}] #

		item['post_link'] = response.link

		item['post_content'] = post.xpath('.//div[startswith(@class,"post")]/blockquote/text()').extract()

		item['post_timestamp'] = post_info.xpath('.//span[@class="dateTime"]/@data-utc').extract_first()
		# if UTC does not work just add /text() instead of @data-utc

		item['post_userid'] = post_info.xpath('.//span[@class="nameBlock"]/span[startswith(@class,"post'
												+ 'eruid ")]/..//text()').extract_first()

		item['post_subject'] = post_info.xpath('.//span[@class="nameBlock"]/span/[@class'
												+ '="Subject"]/..//text()').extract_first()

		item['post_id'] = post_info.xpath('.//span[@class="dateTime"]/a[contains(@title'
												+ ',"Reply to ")]/text()').extract_first()

		for thread in thread_replies:
			pass
