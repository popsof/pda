from django.conf.urls import url
from . import views

app_name = 'cal'

urlpatterns = [
    url(r'^timezone/set/$', views.timezone_set, name='timezone_set'),
    url(r'^month/$', views.this_month, name='this_month'),
    url(r'^month/(\d+)/(\d+)/$', views.cal_month, name='cal_month'),
    url(r'^month/(\d+)/(\d+)/set_memo/(\d+)/$', views.set_memo, name='set_memo'),
    url(r'^year/$', views.this_year, name='this_year'),
    url(r'^year/(\d+)/$', views.cal_year, name='cal_year'),
    url(r'^$', views.cal_main, name='cal_main'),


    url(r'^flood/month/$', views.flood_this_month, name='flood_this_month'),
    url(r'^flood/month/(\d+)/(\d+)/$', views.flood_month, name='flood_month'),
    url(r'^flood/prev_month/(\d+)/(\d+)/$', views.prev_month, name='prev_month'),
    url(r'^flood/next_month/(\d+)/(\d+)/$', views.next_month, name='next_month'),

    url(r'^flood/year/$', views.flood_this_year, name='flood_this_year'),
    url(r'^flood/year/(\d+)/$', views.flood_year, name='flood_year'),
    url(r'^flood/prev_year/(\d+)/(\d+)/$', views.prev_year, name='prev_year'),
    url(r'^flood/next_year/(\d+)/(\d+)/$', views.next_year, name='next_year'),
]

