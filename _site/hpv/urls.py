from django.conf.urls import url
from .views import hours_per_unit, logout_view, Detail
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/hours_per_unit/', permanent=False),
        name='redirect'),
    url(r'^hours_per_unit/$', hours_per_unit.as_view(), name="hours_per_unit"),
    url(r'^detail/', Detail.as_view()),
    url(r'^logout/$', logout_view),
]
