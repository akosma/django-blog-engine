import os.path
from django.conf.urls.defaults import *
from blog.engine import views
from blog.engine.feeds import Atom, RSS2, RSS091

feeds = {
    'atom': Atom,
    'rss': RSS2,
    'rss091': RSS091
}

urlpatterns = patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^$', views.index),
    (r'^(\d{1,4})$', views.post_by_id),
    (r'^(\d{4})/(\d{2})/(\d{2})/(.*)$', views.post_by_date_and_slug),
    (r'^post/(\d{1,4})/comments/add$', views.add_comment),
    (r'^tag/(.*)/$', views.posts_by_tag),

    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
            {'feed_dict': feeds}),

    ( r'^static/(?P<path>.*)$', 'django.views.static.serve', 
            { 'document_root': os.path.join(os.path.dirname(__file__), 'media').replace('\\','/') } ),
)
