from django.db import models
from django.utils import timezone
import datetime as dt


# Rename to Plant Settings
class PlantSetting(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    plant_code = models.CharField(max_length=3, default="017", help_text="Three Digit Plant ID")
    plant_target = models.IntegerField(default=55, help_text="Number of trucks per shift")
    num_of_shifts = models.IntegerField(default=2, help_text="Number of active shifts. (1, 2, or 3)")
    TAKT_Time = models.IntegerField(default=15, help_text="Maximum time between server data points. (In Minutes)")
    CHK_SRVR = models.IntegerField(default=5, help_text="How often to poll the claim server for claimed truck. (In Minutes)")
    del_after = models.IntegerField(default=45, help_text="How long to keep calulated in on server. (In Days)")
    first_shift = models.TimeField(default=dt.time(6, 30), null=True,
                                   blank=True, help_text="In HH:MM:SS")
    second_shift = models.TimeField(default=dt.time(14, 30), null=True,
                                    blank=True, help_text="In HH:MM:SS")
    third_shift = models.TimeField(default=dt.time(22, 30), null=True,
                                   blank=True, help_text="In HH:MM:SS")
    with timezone.override("US/Eastern"):
        dripper_start = models.DateTimeField(default=timezone.make_aware(
                                    dt.datetime(2016, 4, 1, 0, 0)))
