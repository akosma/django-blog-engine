from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed, RssUserland091Feed, Rss201rev2Feed
from engine.models import Post

class Atom(Feed):
    feed_type = Atom1Feed
    title = "Latest blog entries"
    link = "/"
    description = "Updates on the latest blog entries!"

    def items(self):
        return Post.objects.all()[:10]

class RSS091(Atom):
    feed_type = RssUserland091Feed

class RSS2(Atom):
    feed_type = Rss201rev2Feed
