# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from posts.models import Post


class MetanewscrawlerItem(DjangoItem):
    django_model = Post
