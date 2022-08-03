import scrapy
from ..items import MetanewscrawlerItem
from scrapy.http import Response, Request
from users.models import Profile


class TechnologySpider(scrapy.Spider):
    name = 'entertainment_spider'
    start_urls = [
        'https://www.republicworld.com/entertainment-news'
    ]

    def parse(self, response: Response, **kwargs):
        links = response.css('.story-box a::attr(href)').extract()
        for link in links:
            yield Request(url=link,
                          callback=self.parse_link,
                          dont_filter=False,
                          cb_kwargs={'temp_dict': None})

    def parse_link(self, response: Response, temp_dict):
        item = MetanewscrawlerItem()
        title = response.css('.story-title::text').extract_first().replace('\n', '').replace('\\', '').strip()
        description = ' '.join(response.css('.storytext div > p::text').extract()).replace('\n', '').replace('\\', '').strip()
        image = response.css('.storypicture img::attr(src)').extract()[2]
        item['topic'] = 'entertainment'
        item['title'] = title
        item['description'] = description
        item['image'] = image
        item['author'] = Profile.objects.get(name='euronews')
        yield item
