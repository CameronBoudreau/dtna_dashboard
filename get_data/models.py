from django.db import models
import datetime
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
import re



class EmpClockDataModel(models.Model):
    EMP_ID_TXT = models.CharField(max_length=100)
    EMP_NAME = models.TextField()
    EMP_DEPT_TXT = models.TextField()
    CLOCK_IN_REASON = models.CharField(max_length=100, null=True)
    CLOCK_IN_TIME = models.DateTimeField(null=True, blank=True)
    CLOCK_OUT_REASON = models.CharField(max_length=100, null=True)
    CLOCK_OUT_TIME = models.DateTimeField(null=True, blank=True)


# Claims Data
class PlantActivityModel(models.Model):
    UNIT_NUM = models.CharField(max_length=6)
    UNIT_LOADED_TIME = models.DateTimeField()
    UNIT_COMPLETED_DEPT = models.CharField(max_length=10)


# Based on the Mount Holly Org Updates 2015 Excel File
class OrgUnits(models.Model):
    DEPT_NAME = models.CharField(max_length=255)
    DEPT_ABRV = models.CharField(max_length=5)
    DEPT_ID = models.CharField(max_length=100)
    SHIFT_ID = models.CharField(max_length=10)
