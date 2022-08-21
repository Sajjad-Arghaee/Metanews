import scrapy
from ..items import MetanewscrawlerItem
from scrapy.http import Response, Request
from users.models import Profile


class TechnologySpider(scrapy.Spider):
    name = 'metaverse_spider2'
    start_urls = [
        'https://www.xrtoday.com/tag/metaverse/'
    ]

    def parse(self, response: Response, **kwargs):
        links = response.css('.mr-0 a::attr(href)').extract()
        for link in links:
            yield Request(url=link,
                          callback=self.parse_link,
                          dont_filter=False,
                          cb_kwargs={'temp_dict': None})

    def parse_link(self, response: Response, temp_dict):
        item = MetanewscrawlerItem()
        title = response.css('.mt-0::text').extract_first().replace('\n', '').replace('\\', '').strip()
        description = ' '.join(response.css('.post_body h2 , .post_body > p::text').extract()).replace('\n', '').replace('\\', '').strip()
        image = response.css('img.mb-30::attr(src)').extract_first()
        item['topic'] = 'metaverse'
        item['title'] = title
        item['description'] = description
        item['image'] = image
        item['author'] = Profile.objects.get(name='xrtoday')
        yield item
