from django.conf.urls import url
from .views import Clone, hours_per_unit
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^', Clone.as_view()),
    url(r'^planthours_per_unit/$', hours_per_unit.as_view(), name="plant_hours_per_unit"),
]
