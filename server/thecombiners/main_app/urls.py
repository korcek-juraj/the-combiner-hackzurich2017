from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^run_car/$', views.run_car, name='run_car'),
    url(r'^get_car_status/$', views.get_car_status, name='get_car_status'),
]