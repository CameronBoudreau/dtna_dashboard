from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
   url(r'^api/hours_per_unit', views.hours_per_unitAPI.as_view()),
]
