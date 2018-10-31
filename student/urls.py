from django.conf.urls import include, url
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static  
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.home, name='home'),
    #url(r'^/register/$', views.signup, name='signup'),
    url(r'^/login/$', views.signin, name='signin'),
    url(r'^/signup/$', views.signup, name='signup'),
    url(r'^/register/$', views.signup, name='signup'),
    url(r'^/info/$', views.studentinfo, name='studentinfo'),
    url(r'^/error/$', views.error, name='error'),
    url(r'^/dashboard/$', views.dashboard, name='dashboard'),
    url(r'^/logout/$', views.site_logout, name='logout'),
    url(r'^/order/$', views.order, name='order'),
    url(r'^/blog/$', views.blog, name='blog'),
    #url(r'^/control/$', views.control, name='control'),
    url(r'^/checkout/$', views.checkout, name='control'),
    url(r'^/order/(?P<event_id>[0-9]+)/$', views.preorder, name='preorder'),
    url(r'^/dashboard/cancel/$', views.cancel, name='cancel'),
    url(r'^/forgot/$', views.forgot, name='forgot'),
    #url(r'^/change/$', views.change, name='change'),
    url(r'^/control/$', views.change, name='change'),
    url(r'^/display/$', views.display, name='display'),
    url(r'^/distribution/$', views.distribution, name='distribution'),
    url(r'^/credits/$', views.credits, name='credits'),
]
#]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
