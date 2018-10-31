from django.conf.urls import include, url
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.forgotpassword, name='forgotpassword'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
