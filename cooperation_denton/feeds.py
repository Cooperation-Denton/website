# django_project/feeds.py
from django.contrib.syndication.views import Feed

from blog.models import Post


class BlogFeeds(Feed):
    title = "Cooperation Denton Blog"
    link = "/blog/"
    description = "The blog of Cooperation Denton."

    def items(self):
        return Post.objects.order_by("-updated_on")[:100]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_lastupdated(self, item):
        return item.updated_on
