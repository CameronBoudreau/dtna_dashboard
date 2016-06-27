from api.models import hours_per_unitATM
from get_data.models import EmpClockDataModel, PlantActivityModel
from plantsettings.models import PlantSetting
from django.utils import timezone
import datetime as dt


@timezone.override('US/Eastern')
def turn_back(*args, **kwargs):
    last_time = timezone.make_aware(dt.datetime(*args, **kwargs))
    hours_per_unitATM.objects.filter(timestamp__gt=last_time).delete()
    PlantActivityModel.objects.filter(UNIT_LOADED_TIME__gt=last_time).delete()
    for i in EmpClockDataModel.objects.filter(CLOCK_OUT_TIME__gt=last_time):
        i.CLOCK_OUT_TIME = None
        i.CLOCK_OUT_REASON = "&missedOut"
        i.save()
    for i in EmpClockDataModel.objects.filter(CLOCK_IN_TIME__gt=last_time):
        i.CLOCK_IN_TIME = None
        i.CLOCK_IN_REASON = None
        i.CLOCK_OUT_TIME = None
        i.CLOCK_OUT_REASON = None
        i.save()
    i = PlantSetting.objects.first()
    i.dripper_start = last_time
    i.save()
