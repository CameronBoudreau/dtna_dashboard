from django.db import models
import datetime


class Attendance(models.Model):
    employee_number = models.IntegerField()
    department = models.CharField(max_length=16)
    clock_in_time = models.DateTimeField()
    clock_out_time = models.DateTimeField(null=True, blank=True)
    shift = models.CharField(max_length=16)

    @staticmethod
    def get_manhours_during(start, stop=None, department='all', shift='all'):
        if stop is None:
            stop = datetime.datetime.now()
        if shift == 'all':
            this_shift = Attendance.objects.all()
        else:
            this_shift = Attendance.objects.filter(shift=shift)
        if department == 'all' or department == 'Plant':
            in_department = this_shift
        else:
            in_department = this_shift.filter(department=department)
        were_clocked_in = in_department.filter(clock_in_time__lt=start).exclude(clock_out_time__lt=start)
        clocked_in_after_start = in_department.filter(clock_in_time__gte=start)
        clocked_in_during = clocked_in_after_start.filter(clock_in_time__lt=stop)
        clocked_out_after_start = in_department.filter(clock_out_time__gte=start)
        clocked_out_during = clocked_out_after_start.filter(clock_out_time__lt=stop)
        all_relevent = were_clocked_in | clocked_in_during | clocked_out_during
        manhours = 0
        for employee in all_relevent:
            begin = max(employee.clock_in_time, start)
            if employee.clock_out_time == None:
                end = stop
            else:
                end = min(employee.clock_out_time, stop)
            manhours += ((end - begin).total_seconds())/3600
        return manhours


    @staticmethod
    def get_active_at(active_time=None, department='all', shift='all'):
        if active_time is None:
            active_time = datetime.datetime.now()
        if shift == 'all':
            this_shift = Attendance.objects.all()
        else:
            this_shift = Attendance.objects.filter(shift=shift)
        if department == 'all' or department == 'Plant':
            in_department = this_shift
        else:
            in_department = this_shift.filter(department=department)
        have_clocked_in = in_department.filter(clock_in_time__lt=active_time)
        not_clocked_out_yet = have_clocked_in.filter(clock_out_time__gt=active_time)
        never_clocked_out = have_clocked_in.filter(clock_out_time=None)
        not_clocked_out = not_clocked_out_yet | never_clocked_out
        return not_clocked_out.count()

    def is_ot(self, time_in_question=None):
        if time_in_question is None:
            time_in_question = datetime.datetime.now().time()
        if self.shift == 0:
            if not self.clock_out_time and time_in_question > datetime.time(14, 30):
                return True
            else:
                return False
        else:
            if not self.clock_out_time and time_in_question > datetime.time(22, 30):
                return True
            else:
                return False


class Complete(models.Model):
    serial_number = models.CharField(max_length=10)
    completed = models.DateTimeField()

    @staticmethod
    def claims_by_time(time_in_question, hour=None):
        day = time_in_question.date()
        return Complete.objects.filter(completed__gt=datetime.datetime.combine(day,
                datetime.time(0))).filter(completed__lt=time_in_question).count()
