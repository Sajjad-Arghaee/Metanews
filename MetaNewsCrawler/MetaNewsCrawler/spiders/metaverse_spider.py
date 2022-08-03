import scrapy
from ..items import MetanewscrawlerItem
from users.models import Profile


class MetaverseSpiderSpider(scrapy.Spider):
    name = 'metaverse_spider'
    start_urls = [
        'https://www.euronews.com/tag/metaverse'
    ]

    def parse(self, response, **kwargs):
        item = MetanewscrawlerItem()
        all_data = response.css('#c-search-articles .m-object--has-related')
        for data in all_data:
            title = data.css('a[rel="bookmark"]::text').extract_first().replace('\n', '').replace('\\', '').strip()
            description = data.css('.m-object__description__link::text').extract_first().replace('\\', '').strip()
            image = data.css('.m-img.lazyload::attr(data-src)').extract_first()
            item['topic'] = 'metaverse'
            item['title'] = title
            item['description'] = description
            item['image'] = image
            item['author'] = Profile.objects.get(name='euronews')
            yield item
