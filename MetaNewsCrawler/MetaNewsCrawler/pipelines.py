from scrapy_djangoitem import DjangoItem
from posts.models import Post, Tag
from users.models import Profile
from monkeylearn import MonkeyLearn


class MetanewscrawlerPipeline:
    def process_item(self, item: DjangoItem, spider):
        obj = item.save(commit=False)
        try:
            post = Post.objects.get(title=obj.title)
        except Exception:
            post = None
        if not post:
            if obj.author.name == 'euronews':
                euro_news = Profile.objects.get(name='euronews')
                euro_news.active_posts += 1
                euro_news.save()
            else:
                xrtoday = Profile.objects.get(name='xrtoday')
                xrtoday.active_posts += 1
                xrtoday.save()
            post = item.save()
            ml = MonkeyLearn('4201683e97f0c1d475d3a466097c0e63e8082c54')
            data = [post.title]
            model_id = 'ex_YCya9nrn'
            result = ml.extractors.extract(model_id, data)
            data_dict = result.body
            extracted_tags = []
            for item in data_dict[0]['extractions'][:5]:
                line = item['parsed_value'].split()
                extracted_tags.extend(line)
            print(extracted_tags)
            for tag in extracted_tags:
                tag_obj, created = Tag.objects.get_or_create(name=tag)
                t = Tag.objects.get(name=tag)
                p = Post.objects.get(title=obj.title)
                p.tags.add(t)

        return item
