from django.db import models, transaction
from hours_per_unit.models import Attendance, Complete
import datetime as dt
from django.utils import timezone
from get_data.models import EmpClockDataModel, PlantActivityModel
# Model._meta.get_all_field_names()


class AttendanceDripper(models.Model):
    employee_number = models.IntegerField()
    department = models.CharField(max_length=16)
    clock_in_time = models.DateTimeField()
    clock_out_time = models.DateTimeField(null=True, blank=True)
    shift = models.CharField(max_length=16)
    create_at = models.DateTimeField()
    edit_1_at = models.DateTimeField(null=True)
    target = Attendance
    last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))

    @classmethod
    def load_from_target(cls):
        for entry in cls.target.objects.all():
            AttendanceDripper.objects.create(employee_number=entry.employee_number,
                                             department=entry.department,
                                             clock_in_time=entry.clock_in_time,
                                             clock_out_time=entry.clock_out_time,
                                             shift=entry.shift,
                                             create_at=entry.clock_in_time,
                                             edit_1_at=entry.clock_out_time)

    @classmethod
    def _create_on_target(cls, stop):
        relevant = cls.objects.filter(create_at__gt=cls.last_drip)
        relevant = relevant.filter(create_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.create(employee_number=entry.employee_number,
                                      department=entry.department,
                                      clock_in_time=entry.clock_in_time,
                                      clock_out_time=None,
                                      shift=entry.shift,)

    @classmethod
    def _edit_1_on_target(cls, stop):
        relevant = cls.objects.filter(edit_1_at__gt=cls.last_drip)
        relevant = relevant.filter(edit_1_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.filter(employee_number=entry.employee_number,
                                      clock_in_time=entry.clock_in_time).update(
                                      clock_out_time=entry.clock_out_time)

    @classmethod
    def update_target(cls, *args, **kwargs):
        cls._create_on_target(*args, **kwargs)
        cls._edit_1_on_target(*args, **kwargs)
        if "stop" in kwargs:
            stop = kwargs['stop']
        else:
            stop = args[0]
        cls.last_drip = stop


class CompleteDripper(models.Model):
    serial_number = models.CharField(max_length=10)
    completed = models.DateTimeField()
    create_at = models.DateTimeField()
    target = Complete
    last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))

    @classmethod
    def load_from_target(cls):
        for entry in cls.target.objects.order_by('pk'):
            cls.objects.create(serial_number=entry.serial_number,
                               completed=entry.completed,
                               create_at=entry.completed)

    @classmethod
    def _create_on_target(cls, stop):
        relevant = cls.objects.filter(create_at__gt=cls.last_drip)
        relevant = relevant.filter(create_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.create(serial_number=entry.serial_number,
                                      completed=entry.completed)

    @classmethod
    def update_target(cls, *args, **kwargs):
        cls._create_on_target(*args, **kwargs)
        if "stop" in kwargs:
            stop = kwargs['stop']
        else:
            stop = args[0]
        cls.last_drip = stop


class EmpClockDataModelDripper(models.Model):
    EMP_ID_TXT = models.CharField(max_length=100)
    EMP_NAME = models.TextField()
    EMP_DEPT_TXT = models.TextField()
    CLOCK_IN_REASON = models.CharField(max_length=100, null=True)
    CLOCK_IN_TIME = models.DateTimeField(null=True, blank=True)
    CLOCK_OUT_REASON = models.CharField(max_length=100, null=True)
    CLOCK_OUT_TIME = models.DateTimeField(null=True, blank=True)
    create_at = models.DateTimeField(null=True)
    edit_1_at = models.DateTimeField(null=True)
    edit_2_at = models.DateTimeField(null=True)
    target = EmpClockDataModel
    try:
        if target.objects.exists():
            last_drip = max(target.objects.filter(CLOCK_IN_TIME__isnull=False).latest('CLOCK_IN_TIME').CLOCK_IN_TIME,
                        target.objects.filter(CLOCK_OUT_TIME__isnull=False).latest('CLOCK_OUT_TIME').CLOCK_OUT_TIME)
        else:
            last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))
    except:
        last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))

    @classmethod
    def load_from_target(cls):
        with timezone.override("US/Eastern"):
            earliest_time = timezone.localtime(cls.target.objects.earliest('CLOCK_IN_TIME').CLOCK_IN_TIME)
            for entry in cls.target.objects.order_by('pk'):
                if entry.CLOCK_IN_REASON in [None, "&newShift"]:
                    create_time = dt.datetime.combine(earliest_time, dt.time(hour=3))
                    create_time = timezone.make_aware(create_time)
                else:
                    create_time = entry.CLOCK_IN_TIME
                cls.objects.create(EMP_ID_TXT=entry.EMP_ID_TXT,
                                   EMP_NAME=entry.EMP_NAME,
                                   EMP_DEPT_TXT=entry.EMP_DEPT_TXT,
                                   CLOCK_IN_REASON=entry.CLOCK_IN_REASON,
                                   CLOCK_IN_TIME=entry.CLOCK_IN_TIME,
                                   CLOCK_OUT_REASON=entry.CLOCK_OUT_REASON,
                                   CLOCK_OUT_TIME=entry.CLOCK_OUT_TIME,
                                   create_at=create_time,
                                   edit_1_at=entry.CLOCK_IN_TIME,
                                   edit_2_at=entry.CLOCK_OUT_TIME)
                if entry.CLOCK_IN_TIME is not None:
                    earliest_time = entry.CLOCK_IN_TIME

    @classmethod
    def _create_on_target(cls, stop):
        relevant = cls.objects.filter(create_at__gt=cls.last_drip)
        relevant = relevant.filter(create_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.create(EMP_ID_TXT=entry.EMP_ID_TXT,
                                      EMP_NAME=entry.EMP_NAME,
                                      EMP_DEPT_TXT=entry.EMP_DEPT_TXT,
                                      CLOCK_IN_REASON=None,
                                      CLOCK_IN_TIME=None,
                                      CLOCK_OUT_REASON=None,
                                      CLOCK_OUT_TIME=None)

    @classmethod
    def _edit_1_on_target(cls, stop):
        relevant = cls.objects.filter(edit_1_at__gt=cls.last_drip)
        relevant = relevant.filter(edit_1_at__lte=stop)
        for entry in relevant.order_by('pk'):
            to_update = cls.target.objects.filter(EMP_ID_TXT=entry.EMP_ID_TXT,
                                                  EMP_NAME=entry.EMP_NAME,
                                                  EMP_DEPT_TXT=entry.EMP_DEPT_TXT).last()
            if to_update:
                to_update.CLOCK_IN_TIME = entry.CLOCK_IN_TIME
                to_update.CLOCK_IN_REASON = entry.CLOCK_IN_REASON
                to_update.CLOCK_OUT_REASON = "&missedOut"
                to_update.save()

    @classmethod
    def _edit_2_on_target(cls, stop):
        relevant = cls.objects.filter(edit_2_at__gt=cls.last_drip)
        relevant = relevant.filter(edit_2_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.filter(EMP_DEPT_TXT=entry.EMP_DEPT_TXT,
                                      CLOCK_IN_TIME=entry.CLOCK_IN_TIME).update(
                                      CLOCK_OUT_REASON=entry.CLOCK_OUT_REASON,
                                      CLOCK_OUT_TIME=entry.CLOCK_OUT_TIME)

    @classmethod
    def update_target(cls, *args, **kwargs):
        cls._create_on_target(*args, **kwargs)
        cls._edit_1_on_target(*args, **kwargs)
        cls._edit_2_on_target(*args, **kwargs)
        if "stop" in kwargs:
            stop = kwargs['stop']
        else:
            stop = args[0]
        cls.last_drip = stop


class PlantActivityModelDripper(models.Model):
    UNIT_NUM = models.CharField(max_length=6)
    UNIT_COMPLETED_DEPT = models.CharField(max_length=10)
    UNIT_LOADED_TIME = models.DateTimeField()
    create_at = models.DateTimeField()
    target = PlantActivityModel
    try:
        if target.objects.exists():
            last_drip = target.objects.filter(UNIT_LOADED_TIME__isnull=False).latest('UNIT_LOADED_TIME').UNIT_LOADED_TIME
        else:
            last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))
    except:
        last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))

    @classmethod
    def load_from_target(cls):
        for entry in cls.target.objects.all():
            cls.objects.create(UNIT_NUM=entry.UNIT_NUM,
                               UNIT_COMPLETED_DEPT=entry.UNIT_COMPLETED_DEPT,
                               UNIT_LOADED_TIME=entry.UNIT_LOADED_TIME,
                               create_at=entry.UNIT_LOADED_TIME
                               )

    @classmethod
    def _create_on_target(cls, stop):
        relevant = cls.objects.filter(create_at__gt=cls.last_drip)
        relevant = relevant.filter(create_at__lte=stop)
        for entry in relevant.order_by('pk'):
            cls.target.objects.create(UNIT_NUM=entry.UNIT_NUM,
                                      UNIT_COMPLETED_DEPT=entry.UNIT_COMPLETED_DEPT,
                                      UNIT_LOADED_TIME=entry.UNIT_LOADED_TIME,
                                      )
    @classmethod
    def update_target(cls, *args, **kwargs):
        cls._create_on_target(*args, **kwargs)
        if "stop" in kwargs:
            stop = kwargs['stop']
        else:
            stop = args[0]
        cls.last_drip = stop


class CombinedDripper:
    drippers = []

    def __init__(self, start_time, time_step=dt.timedelta(minutes=5)):
        self.simulated_time = start_time
        self.time_step = time_step

    def add_dripper(self, *args):
        for dripper in args:
            if dripper not in self.drippers:
                self.drippers.append(dripper)
                dripper.update_target(self.simulated_time)

    def update_to(self, new_time):
        for dripper in self.drippers:
            dripper.update_target(new_time)
        self.simulated_time = new_time

    def update_by(self, time_step):
        new_time = self.simulated_time + time_step
        self.update_to(new_time)

    @transaction.atomic()
    def update(self):
        self.update_by(self.time_step)

    def clear_targets(self):
        for dripper in self.drippers:
            dripper.target.objects.all().delete()
            dripper.last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))

    def load_drippers(self):
        for dripper in self.drippers:
            dripper.load_from_target()

    def clear_drippers(self):
        for dripper in self.drippers:
            dripper.objects.all().delete()


#######################################################
# Unused models
#######################################################
# class RawCrysDataDripper(models.Model):
#     DEPT8_ITEM_DSCREP_ID = models.CharField(max_length=255)
#     DEPT8_INSP_ITEM_ID = models.CharField(max_length=255)
#     UNIT_NUM = models.CharField(max_length=6)
#     FOUND_INSP_TEAM = models.CharField(max_length=3)
#     INSP_DSCREP_DESC = models.CharField(max_length=255)
#     INSP_COMT = models.TextField()
#     UNIT_LOADED_TIME = models.DateTimeField()
#     create_at = models.DateTimeField()
#     target = RawCrysData
#     last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))
#
#     @classmethod
#     def load_from_target(cls):
#         for entry in cls.target.objects.all():
#             cls.objects.create(DEPT8_ITEM_DSCREP_ID=entry.DEPT8_ITEM_DSCREP_ID,
#                                DEPT8_INSP_ITEM_ID=entry.DEPT8_INSP_ITEM_ID,
#                                UNIT_NUM=entry.UNIT_NUM,
#                                FOUND_INSP_TEAM=entry.FOUND_INSP_TEAM,
#                                INSP_DSCREP_DESC=entry.INSP_DSCREP_DESC,
#                                INSP_COMT=entry.INSP_COMT,
#                                UNIT_LOADED_TIME=entry.UNIT_LOADED_TIME,
#                                create_at=entry.UNIT_LOADED_TIME
#                                )
#
#     @classmethod
#     def _create_on_target(cls, stop):
#         relevant = cls.objects.filter(create_at__gt=cls.last_drip)
#         relevant = relevant.filter(create_at__lte=stop)
#         for entry in relevant.order_by('pk'):
#             cls.target.objects.create(DEPT8_ITEM_DSCREP_ID=entry.DEPT8_ITEM_DSCREP_ID,
#                                       DEPT8_INSP_ITEM_ID=entry.DEPT8_INSP_ITEM_ID,
#                                       UNIT_NUM=entry.UNIT_NUM,
#                                       FOUND_INSP_TEAM=entry.FOUND_INSP_TEAM,
#                                       INSP_DSCREP_DESC=entry.INSP_DSCREP_DESC,
#                                       INSP_COMT=entry.INSP_COMT,
#                                       UNIT_LOADED_TIME=entry.UNIT_LOADED_TIME
#                                       )
#
#     @classmethod
#     def update_target(cls, *args, **kwargs):
#         cls._create_on_target(*args, **kwargs)
#         if "stop" in kwargs:
#             stop = kwargs['stop']
#         else:
#             stop = args[0]
#         cls.last_drip = stop
#
# class RawDirectRunDataDripper(models.Model):
#     UNIT_NUM = models.CharField(max_length=6)
#     UNIT_LOADED_TIME = models.DateTimeField()
#     SHIFT = models.IntegerField()
#     DEPT8 = models.IntegerField()
#     PAINT = models.IntegerField()
#     SH = models.IntegerField()
#     ENG_SC = models.IntegerField()
#     create_at = models.DateTimeField()
#     target = RawDirectRunData
#     last_drip = timezone.make_aware(dt.datetime(1, 1, 1, 0, 0))
#
#     @classmethod
#     def load_from_target(cls):
#         for entry in cls.target.objects.all():
#             cls.objects.create(UNIT_NUM=entry.UNIT_NUM,
#                                UNIT_LOADED_TIME=entry.UNIT_LOADED_TIME,
#                                SHIFT=entry.SHIFT,
#                                DEPT8=entry.DEPT8,
#                                PAINT=entry.PAINT,
#                                SH=entry.SH,
#                                ENG_SC=entry.ENG_SC,
#                                create_at=entry.UNIT_LOADED_TIME
#                                )
#
#     @classmethod
#     def _create_on_target(cls, stop):
#         relevant = cls.objects.filter(create_at__gt=cls.last_drip)
#         relevant = relevant.filter(create_at__lte=stop)
#         for entry in relevant.order_by('pk'):
#             cls.target.objects.create(UNIT_NUM=entry.UNIT_NUM,
#                                       UNIT_LOADED_TIME=entry.UNIT_LOADED_TIME,
#                                       SHIFT=entry.SHIFT,
#                                       DEPT8=entry.DEPT8,
#                                       PAINT=entry.PAINT,
#                                       SH=entry.SH,
#                                       ENG_SC=entry.ENG_SC)
#
#     @classmethod
#     def update_target(cls, *args, **kwargs):
#         cls._create_on_target(*args, **kwargs)
#         if "stop" in kwargs:
#             stop = kwargs['stop']
#         else:
#             stop = args[0]
#         cls.last_drip = stop
#
