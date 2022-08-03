from scrapy_djangoitem import DjangoItem
from posts.models import Post
from users.models import Profile


class MetanewscrawlerPipeline:
    def process_item(self, item: DjangoItem, spider):
        if spider.name == 'metaverse_spider':
            obj = item.save(commit=False)
            try:
                post = Post.objects.get(title=obj.title)
            except Exception:
                post = None
            if not post:
                euro_news = Profile.objects.get(name='euronews')
                euro_news.active_posts += 1
                euro_news.save()
                item.save()
            return item
        elif spider.name == 'technology_spider' or spider.name == 'sports_spider':
            obj = item.save(commit=False)
            try:
                post = Post.objects.get(title=obj.title)
            except Exception:
                post = None
            if not post:
                euro_news = Profile.objects.get(name='euronews')
                euro_news.active_posts += 1
                euro_news.save()
                item.save()
            return item
        else:
            return None
