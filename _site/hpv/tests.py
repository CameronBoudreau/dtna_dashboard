from django.test import TestCase
from .models import Attendance
import datetime as dt
import pytz


class AttendanceTestCase(TestCase):

    def setUp(self):
        # first shift clocked out
        Attendance.objects.create(employee_number=66661,
                                  department='DEPT1',
                                  clock_in_time=dt.datetime(2016, 6, 1, 6, 30),
                                  clock_out_time=dt.datetime(2016, 6, 1, 14,
                                                             30),
                                  shift='first')

        # first shift not clocked out
        Attendance.objects.create(employee_number=66662,
                                  department='DEPT5',
                                  clock_in_time=dt.datetime(2016, 6, 1, 6, 30),
                                  clock_out_time=None,
                                  shift='first')

        # second shift clocked out
        Attendance.objects.create(employee_number=66663,
                                  department='DEPT2',
                                  clock_in_time=dt.datetime(2016, 6, 1, 14,
                                                            30),
                                  clock_out_time=dt.datetime(2016, 6, 1, 22,
                                                             30),
                                  shift='second')

        # second shift not clocked out
        Attendance.objects.create(employee_number=66664,
                                  department='DEPT3',
                                  clock_in_time=dt.datetime(2016, 6, 1, 14,
                                                            30),
                                  clock_out_time=None,
                                  shift='second')

    def test_get_manhours_during_first_shift_plus_1_hour(self):
        start = pytz.utc.localize(dt.datetime(2016, 6, 1, 6, 30))
        stop = pytz.utc.localize(dt.datetime(2016, 6, 1, 15, 30))
        expected_manhours = 19

        manhours = Attendance.get_manhours_during(start, stop)
        self.assertEqual(manhours, expected_manhours)
