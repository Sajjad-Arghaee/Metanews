import scrapy
from ..items import MetanewscrawlerItem
from scrapy.http import Response, Request
from users.models import Profile


class SportsSpider(scrapy.Spider):
    name = 'sports_spider'
    start_urls = [
        'https://www.euronews.com/news/sport'
    ]
    counter = 0

    def parse(self, response: Response, **kwargs):
        links = response.css('.m-modeXL-2 .m-object__title__link::attr(href)').extract()
        temp_dict = {'image': response.css('.m-modeXL-2 .m-img::attr(data-src)').extract()}
        for link in links:
            yield Request(url='https://www.euronews.com/'+link,
                          callback=self.parse_link,
                          dont_filter=False,
                          cb_kwargs={'temp_dict': temp_dict})

    def parse_link(self, response: Response, temp_dict):
        item = MetanewscrawlerItem()
        title = response.css('.u-text-align--start::text').extract_first().replace('\n', '').replace('\\', '').strip()
        description = ' '.join(response.css('.js-article-content p::text').extract()).replace('\n', '').replace('\\', '').strip()
        item['topic'] = 'sports'
        item['title'] = title
        item['description'] = description
        item['image'] = temp_dict['image'][self.counter]
        self.counter += 1
        item['author'] = Profile.objects.get(name='euronews')
        yield item
