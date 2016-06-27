from django.shortcuts import render
from .models import hours_per_unitATM
from .serializers import hours_per_unitSerializer
from rest_framework import generics, renderers, permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Min
import datetime as dt


class hours_per_unitAPI(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = hours_per_unitATM.objects.all()
    serializer_class = hours_per_unitSerializer
    login_url = '/login/'

    def get_queryset(self):
        queryset = hours_per_unitATM.objects.all()

        days = self.request.query_params.get('days', None)
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)
        start_time = queryset.aggregate(Min('timestamp'))['timestamp__min']
        end_time = queryset.aggregate(Max('timestamp'))['timestamp__max']
        if start is not None:
            start_time = dt.datetime.fromtimestamp(int(start), dt.timezone.utc)
        if end is not None:
            end_time = dt.datetime.fromtimestamp(int(end), dt.timezone.utc)
        if days is not None:
            if start is None:
                start_time = end_time - dt.timedelta(days=int(days))
            elif end is None:
                end_time = start_time + dt.timedelta(days=int(days))
        return queryset.filter(timestamp__gte=start_time, timestamp__lte=end_time).order_by('timestamp')

    
