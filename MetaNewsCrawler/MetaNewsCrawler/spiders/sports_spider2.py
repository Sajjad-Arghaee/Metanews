import scrapy
from ..items import MetanewscrawlerItem
from scrapy.http import Response, Request
from users.models import Profile


class SportsSpider2(scrapy.Spider):
    name = 'sports_spider2'
    page_number = 3
    start_urls = [
        'https://www.skysports.com/news-wire/more/1'
    ]

    def parse(self, response: Response, **kwargs):
        links = response.css('.news-list__headline-link::attr(href)').extract()
        for link in links:
            yield Request(url=link,
                          callback=self.parse_link,
                          dont_filter=False,
                          cb_kwargs={'temp_dict': None})

    def parse_link(self, response: Response, temp_dict):
        item = MetanewscrawlerItem()
        title = response.css('.sdc-article-header__long-title::text').extract_first().replace('\n', '').replace('\\', '').strip()
        image = response.css('.sdc-article-image__item::attr(src)').extract_first()
        description = ' '.join(response.css('.sdc-article-body--lead > p::text').extract()).replace('\n', '').replace('\\', '').strip()
        item['topic'] = 'sports'
        item['title'] = title
        item['description'] = description
        item['image'] = image
        item['author'] = Profile.objects.get(name='sky_sports')
        yield item
        next_page = 'https://www.skysports.com/news-wire/more/' + str(SportsSpider2.page_number) + '/'
        if SportsSpider2.page_number < 11:
                SportsSpider2.page_number += 1
                yield response.follow(next_page, callback=self.parse)
