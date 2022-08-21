import scrapy
from ..items import MetanewscrawlerItem
from scrapy.http import Response, Request
from users.models import Profile


class TechnologySpider3(scrapy.Spider):
    name = 'technology_spider3'
    page_number = 2
    start_urls = [
        'https://www.theverge.com/tech/archives/1'
    ]

    def parse(self, response: Response, **kwargs):
        links = response.css('.c-entry-box--compact--article .c-entry-box--compact__title a::attr(href)').extract()
        for link in links:
            yield Request(url=link,
                          callback=self.parse_link,
                          dont_filter=False,
                          cb_kwargs={'temp_dict': None})

    def parse_link(self, response: Response, temp_dict):
        item = MetanewscrawlerItem()
        title = response.css('.c-page-title::text').extract_first().replace('\n', '').replace('\\', '').strip()
        description = ' '.join(response.css('.c-entry-content p::text').extract()).replace('\n', '').replace('\\', '').strip()
        image = response.css('img::attr(src)').extract_first()
        item['topic'] = 'technology'
        item['title'] = title
        item['description'] = description
        item['image'] = image
        item['author'] = Profile.objects.get(name='theverge')
        yield item
        next_page = 'https://www.theverge.com/tech/archives/' + str(TechnologySpider3.page_number) + '/'
        if TechnologySpider3.page_number < 11:
                TechnologySpider3.page_number += 1
                yield response.follow(next_page, callback=self.parse)
