from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from search.views import Main

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', TemplateView.as_view(template_name="base.html")),
                       (r'^result/$', Main.as_view()),

    # Examples:
    # url(r'^$', 'heart.views.home', name='home'),
    # url(r'^heart/', include('heart.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)