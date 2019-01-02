from django.conf.urls import url
from . import views           # This line is new!

app_name = 'wall'
urlpatterns = [
    url(r'^$', views.index, name='my_home'),
    url(r'^success', views.success, name='my_success'),
    url(r'^newsFeed', views.newsFeed, name='my_newsFeed'),
    url(r'^login', views.login, name='my_login'),
    url(r'^register', views.register, name = 'my_register'),
    url(r'^clear$', views.clear, name = 'my_clear'),
    url(r'^send$', views.send, name = 'my_send'),
    url(r'^comment', views.comment, name = 'my_comment'),
    #url(r'^semi_users/(?P<id>\d+)/update$', views.update, name='my_update'),
    #url(r'^semi_users/(?P<id>\d+)/delete$', views.delete, name='my_delete'),
    #url(r'^semi_users/(?P<id>\d+)', views.display, name='my_show'),
]   