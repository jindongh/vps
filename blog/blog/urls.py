from django.conf.urls import patterns, include, url

from django.contrib import admin
from blog import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^weblog/', include('zinnia.urls', namespace='zinnia')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^weixin/help$', 'weixin.views.help'),
    url(r'^weixin/', 'weixin.views.serv'),
    url(r'^store/version', 'store.views.version'),
    url(r'^store/download', 'store.views.download'),
    url(r'^store/', 'store.views.index'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT,}),
)
