from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
import zinnia
import zinnia.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^weblog/', include('zinnia.urls', namespace='zinnia')),
    url(r'^comments/', include('django.contrib.comments.urls')),
)
