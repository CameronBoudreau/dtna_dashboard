from django.conf.urls import url
from . import views

app_name = "dripper"

urlpatterns = [
    url(r'^status/', views.status, name="status"),
    url(r'^load/', views.load, name="load"),
    url(r'^run/', views.run, name='run'),
    # url(r'^stop/', views.stop, name='stop'),
    url(r'^reset/', views.reset, name='reset'),
    url(r'^flush_targets/', views.flush_targets, name='flush_targets'),
    url(r'^flush_drippers/', views.flush_drippers, name='flush_drippers'),
]
