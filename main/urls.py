from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns('',
url(r'^$', views.index, name='index'),
url(r'^(?P<filter_id>\d+)$', views.filtered, name='filtered'),
)

