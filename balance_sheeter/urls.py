from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home$', views.home, name='home'),
    url(r'^save-and-return$', views.save_and_return, name='save-and-return'),
    url(r'^results$', views.results, name='results'),
    url(r'^download$', views.download, name='download'),
    ]