from django.conf.urls import patterns, include, url
import core.views as cv

urlpatterns = patterns('',
    url(r'users/create/$', cv.UserCreateView.as_view(), name='user_ceate'),
    url(r'users/login/$', cv.UserLoginView.as_view(), name='user_login'),
    url(r'sprockets/create/$', cv.SprocketCreateView.as_view(), name='sprocket_create'),
    url(r'sprockets/(?P<instance_id>\d+)/$', cv.SprocketDetailView.as_view(), name='sprocket_detail'),
    url(r'sprockets/(?P<instance_id>\d+)/update/$', cv.SprocketCreateView.as_view(), name='sprocket_create'),
)