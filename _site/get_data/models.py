from django.db import models
from .functions.process_raw_csv_data import *
from .functions.csv_file_paths import *
import datetime
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
import re


"""
This model is intended to hold
all model data for the raw CSV dumps.
"""


class EmpClockDataModel(models.Model):
    EMP_ID_TXT = models.CharField(max_length=100)
    EMP_NAME = models.TextField()
    EMP_DEPT_TXT = models.TextField()
    CLOCK_IN_REASON = models.CharField(max_length=100, null=True)
    CLOCK_IN_TIME = models.DateTimeField(null=True, blank=True)
    CLOCK_OUT_REASON = models.CharField(max_length=100, null=True)
    CLOCK_OUT_TIME = models.DateTimeField(null=True, blank=True)


    @staticmethod
    def load_raw_data():
        # process generator file. CSV has headers.
        # each row is a dict.
        with timezone.override('US/Eastern'):
            for row in read_csv_generator(clock_in_out_csv, headers=True):
                created_row = EmpClockDataModel.objects.create(
                    EMP_ID_TXT=row['EMP_ID_TXT'],
                    EMP_NAME=row['EMP_NAME'],
                    EMP_DEPT_TXT=row['EMP_DEPT_TXT'],
                    CLOCK_IN_REASON=row['CLOCK_IN_REASON'],
                    CLOCK_IN_TIME=process_date(row['PNCHEVNT_DTM_IN']),
                    CLOCK_OUT_REASON=row['CLOCK_OUT_REASON'],
                    CLOCK_OUT_TIME=process_date(row['PNCHEVNT_DTM_OUT']),
                )
                created_row.save()
            print("LOADED Raw Clock Data Row")

# Claims Data
class PlantActivityModel(models.Model):
    UNIT_NUM = models.CharField(max_length=6)
    UNIT_LOADED_TIME = models.DateTimeField()
    UNIT_COMPLETED_DEPT = models.CharField(max_length=10)

    @staticmethod
    def load_raw_data():
        # process generator file. CSV has headers.
        # each row is a dict.
        with timezone.override('US/Pacific'):
            for row in read_csv_generator(plant_activty_csv, headers=True):
                created_row = PlantActivityModel.objects.create(
                    UNIT_NUM=row['UNIT_NUM'],
                    UNIT_COMPLETED_DEPT=row['UNIT_COMPLETED_DEPT'],
                    UNIT_LOADED_TIME=process_date(row['UNIT_LOADED_TIME']),
                )

                created_row.save()
            print("LOADED plant Row")

# Based on the Mount Holly Org Updates 2015 Excel File
class OrgUnits(models.Model):
    DEPT_NAME = models.CharField(max_length=255)
    DEPT_ABRV = models.CharField(max_length=5)
    DEPT_ID = models.CharField(max_length=100)
    SHIFT_ID = models.CharField(max_length=10)

    @staticmethod
    def load_raw_data():
        # process generator file. CSV has headers.
        # each row is a dict.
        for row in read_csv_generator(departments_csv, headers=True):
            created_row = OrgUnits.objects.create(
                DEPT_NAME=row['Name'],
                DEPT_ABRV=row['dept_abvr'],
                DEPT_ID=row['Shift'],
                SHIFT_ID=row['shift_id'],
            )
            created_row.save()
        print("LOADED Department List Row")

#######################################################
# Unused models
#######################################################
# class RawDirectRunData(models.Model):
#     UNIT_NUM = models.CharField(max_length=6)
#     UNIT_LOADED_TIME = models.DateTimeField()
#     SHIFT = models.IntegerField()
#     DEPT8 = models.IntegerField()
#     PAINT = models.IntegerField()
#     SH = models.IntegerField()
#     ENG_SC = models.IntegerField()
#
#     @staticmethod
#     def load_raw_data():
#         # process generator file. CSV has headers.
#         # each row is a dict.
#         raise Exception("Timezone needed")
#         for row in read_csv_generator(direct_run_csv, headers=True):
#             created_row = RawDirectRunData.objects.create(
#                 UNIT_NUM=row['\ufeffUNIT_NUM'],
#                 UNIT_LOADED_TIME=process_date(row['UNIT_LOADED_TIME']),
#                 SHIFT=row['SHIFT'],
#                 DEPT8=row['DEPT8'],
#                 PAINT=row['PAINT'],
#                 SH=row['SH'],
#                 ENG_SC=row['ENG_SC'],
#             )
#             created_row.save()
#         print("LOADED DIRECT RUN Row")
#
#
# class RawCrysData(models.Model):
#     DEPT8_ITEM_DSCREP_ID = models.CharField(max_length=255)
#     DEPT8_INSP_ITEM_ID = models.CharField(max_length=255)
#     UNIT_NUM = models.CharField(max_length=6)
#     FOUND_INSP_TEAM = models.CharField(max_length=3)
#     INSP_DSCREP_DESC = models.CharField(max_length=255)
#     INSP_COMT = models.TextField()
#     UNIT_LOADED_TIME = models.DateTimeField()
#
