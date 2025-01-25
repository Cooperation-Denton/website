# django_project/feeds.py
from django.contrib.syndication.views import Feed

from blog.models import Post


class BlogFeeds(Feed):
    title = "Cooperation Denton Blog"
    link = "/blog/"
    description = "The blog of Cooperation Denton."

    def items(self):
        return Post.objects.filter(is_published=True).order_by("-published_on")[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_pubdate(self, item):
        return item.created_on
