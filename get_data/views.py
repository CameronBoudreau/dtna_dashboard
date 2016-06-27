from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import EmpClockDataModel, PlantActivityModel, OrgUnits
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime as dt
import pytz
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


# Create your views here.
class Clone(TemplateView):
    template_name = "clone/clone.html"

    def get(self, request):
        context = {}
        done = False
        if request.GET.get('clone'):
            EmpClockDataModel.load_raw_data()
            PlantActivityModel.load_raw_data()
            OrgUnits.load_raw_data()
            done=True

        context = {'done': done}
        return render(request, self.template_name, context)

class hours_per_unit(LoginRequiredMixin, TemplateView):
    template_name = "hours_per_unit/hours_per_unit.html"
    login_url = '/login/'
