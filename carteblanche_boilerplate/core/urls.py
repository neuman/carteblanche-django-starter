from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'sprockets/create/$', cv.SprocketCreateView.as_view(), name='project_create'),
    url(r'sprockets/(?P<instance_id>\d+)/$', cv.SprocketDetailView.as_view(), name='project_detail'),
    url(r'sprockets/(?P<instance_id>\d+)/update/$', cv.SprocketCreateView.as_view(), name='pledge_create'),
)