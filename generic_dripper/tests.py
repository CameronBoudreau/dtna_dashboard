from django.test import TestCase
from .models import CompleteDripper, AttendanceDripper, CombinedDripper
from .models import EmpClockDataModelDripper, RawDirectRunDataDripper
from .models import RawCrysDataDripper, PlantActivityModelDripper
from get_data.models import EmpClockDataModel, RawDirectRunData, RawCrysData, PlantActivityModel
from hours_per_unit.models import Complete, Attendance
import datetime as dt
import pytz


class test_dripper_load_one(TestCase):
    time1 = dt.datetime.now(pytz.utc)

    def setUp(self):
        Complete.objects.create(serial_number="1", completed=self.time1)

    def test_load(self):
        CompleteDripper.load_from_target()
        assert(CompleteDripper.objects.count() == 1)
        for entry in CompleteDripper.objects.all():
            assert(entry.serial_number == "1")
            assert(entry.completed == self.time1)
            assert(entry.create_at == self.time1)


class test_dripper_load_many(TestCase):
    time1 = dt.datetime.now(pytz.utc)
    times = []
    for i in range(10):
        times.append(time1 + dt.timedelta(hours=i))
    serial_numbers = [str(x) for x in range(1, 11)]

    def setUp(self):
        for time, serial_number in zip(self.times, self.serial_numbers):
            Complete.objects.create(serial_number=serial_number,
                                    completed=time)

    def test_load(self):
        CompleteDripper.load_from_target()
        assert(CompleteDripper.objects.count() == len(self.times))
        for i, entry in enumerate(CompleteDripper.objects.all()):
            assert(entry.serial_number == self.serial_numbers[i])
            assert(entry.completed == self.times[i])
            assert(entry.create_at == self.times[i])


class test_dripper_one_drip(TestCase):
    time1 = dt.datetime.now(pytz.utc)

    def setUp(self):
        CompleteDripper.objects.create(serial_number="1", completed=self.time1,
                                       create_at=self.time1)
        CompleteDripper.last_drip = dt.datetime(1, 1, 1, 0, 0, tzinfo=pytz.utc)

    def test_one_drip(self):
        one_hour = dt.timedelta(hours=1)
        CompleteDripper.update_target(self.time1 + one_hour)
        self.assertEqual(Complete.objects.count(), 1)
        for entry in Complete.objects.all():
            assert(entry.serial_number == "1")
            assert(entry.completed == self.time1)


class test_dripper_drips(TestCase):
    time1 = dt.datetime.now(pytz.utc)
    times = []
    for i in range(10):
        times.append(time1 + dt.timedelta(hours=i))
    serial_numbers = [str(x) for x in range(1, 11)]

    def setUp(self):
        for time, serial_number in zip(self.times, self.serial_numbers):
            CompleteDripper.objects.create(serial_number=serial_number,
                                           completed=time, create_at=time)
        CompleteDripper.last_drip = dt.datetime(1, 1, 1, 0, 0, tzinfo=pytz.utc)

    def test_small_drips(self):
        for i, t in enumerate(self.times):
            CompleteDripper.update_target(t)
            assert(Complete.objects.count() == i+1)
            for entry, time, serial_number in zip(Complete.objects.all(),
                                                  self.times[:i],
                                                  self.serial_numbers[:i]):
                assert(entry.serial_number == serial_number)
                assert(entry.completed == time)

    def test_big_drips(self):
        for i, t in enumerate(self.times):
            if i != len(self.times)-1 and i % 2 == 0:
                continue
            CompleteDripper.update_target(t)
            assert(Complete.objects.count() == i+1)
            for entry, time, serial_number in zip(Complete.objects.all(),
                                                  self.times[:i],
                                                  self.serial_numbers[:i]):
                assert(entry.serial_number == serial_number)
                assert(entry.completed == time)

    def test_very_small_drips(self):
        last_time = self.time1 - dt.timedelta(hours=1)
        for i, t in enumerate(self.times):
            for j in range(2):
                k = i + j
                if j == 0:
                    small_t = last_time + ((t - last_time) / 2)
                else:
                    small_t = t
                CompleteDripper.update_target(small_t)
                assert(Complete.objects.count() == k)
                for entry, time, serial_number in zip(Complete.objects.all(),
                                                      self.times[:k],
                                                      self.serial_numbers[:k]):
                    assert(entry.serial_number == serial_number)
                    assert(entry.completed == time)
                last_time = small_t


class test_editing_dripper(TestCase):
    time1 = dt.datetime.now(pytz.utc)
    tick_times = []
    for i in range(10):
        tick_times.append(time1 + dt.timedelta(hours=i))
    in_times = []
    for i in range(5):
        in_times.append(time1 + dt.timedelta(minutes=i, hours=i))
        in_times.append(time1 + dt.timedelta(hours=i, minutes=i+30))
    in_times.sort()
    out_times = []
    for i in range(5):
        out_times.append(in_times[i]+dt.timedelta(hours=i))
        out_times.append(None)
    employee_numbers = range(1, 11)

    def setUp(self):
        for in_time, out_time, employee_number in zip(self.in_times,
                                                      self.out_times,
                                                      self.employee_numbers):
            AttendanceDripper.objects.create(employee_number=employee_number,
                                             clock_in_time=in_time,
                                             clock_out_time=out_time,
                                             create_at=in_time,
                                             edit_1_at=out_time)
        AttendanceDripper.last_drip = dt.datetime(1, 1, 1, 0, 0, tzinfo=pytz.utc)

    def test_drips(self):
        for i, t in enumerate(self.tick_times):
            AttendanceDripper.update_target(t)
            self.assertEqual(Attendance.objects.count(), AttendanceDripper.objects.filter(create_at__lte=t).count())
            for entry, in_time, out_time, employee_number in zip(Attendance.objects.order_by('pk'),
                                                                 self.in_times,
                                                                 self.out_times,
                                                                 self.employee_numbers):
                self.assertEqual(entry.employee_number, employee_number)
                self.assertEqual(entry.clock_in_time, in_time)
                if out_time is None or out_time > t:
                    self.assertIsNone(entry.clock_out_time)
                else:
                    self.assertEqual(entry.clock_out_time, out_time)


class test_combined_dripper(TestCase):
    time1 = dt.datetime.now(pytz.utc)
    in_times = []
    for i in range(5):
        in_times.append(time1 + dt.timedelta(minutes=i, hours=i))
        in_times.append(time1 + dt.timedelta(hours=i, minutes=i+30))
    in_times.sort()
    out_times = []
    for i in range(5):
        out_times.append(in_times[i]+dt.timedelta(hours=i))
        out_times.append(None)
    employee_numbers = range(1, 11)
    serial_numbers = [str(x) for x in range(1, 11)]

    def setUp(self):
        for in_time, out_time, employee_number in zip(self.in_times,
                                                      self.out_times,
                                                      self.employee_numbers):
            AttendanceDripper.objects.create(employee_number=employee_number,
                                             clock_in_time=in_time,
                                             clock_out_time=out_time,
                                             create_at=in_time,
                                             edit_1_at=out_time)
        AttendanceDripper.last_drip = dt.datetime(1, 1, 1, 0, 0, tzinfo=pytz.utc)
        for time, serial_number in zip(self.in_times, self.serial_numbers):
            CompleteDripper.objects.create(serial_number=serial_number,
                                           completed=time, create_at=time)
        CompleteDripper.last_drip = dt.datetime(1, 1, 1, 0, 0, tzinfo=pytz.utc)
        self.master_dripper = CombinedDripper(start_time=self.time1 - dt.timedelta(minutes=7))
        self.master_dripper.add_dripper(AttendanceDripper, CompleteDripper)

    def test_update_to(self):
        new_time = self.in_times[5]
        self.assertEqual(Complete.objects.count(), 0)
        self.assertEqual(Attendance.objects.count(), 0)
        self.master_dripper.update_to(new_time)
        self.assertEqual(Complete.objects.count(), 6)
        self.assertEqual(Attendance.objects.count(), 6)
        for entry, time, serial_number in zip(Complete.objects.order_by('pk'),
                                              self.in_times,
                                              self.serial_numbers):
            assert(entry.serial_number == serial_number)
            assert(entry.completed == time)
        for entry, in_time, out_time, employee_number in zip(Attendance.objects.order_by('pk'),
                                                             self.in_times,
                                                             self.out_times,
                                                             self.employee_numbers):
            self.assertEqual(entry.employee_number, employee_number)
            self.assertEqual(entry.clock_in_time, in_time)
            if out_time is None or out_time > new_time:
                self.assertIsNone(entry.clock_out_time)
            else:
                self.assertEqual(entry.clock_out_time, out_time)
        self.assertEqual(new_time, self.master_dripper.simulated_time)

    def test_update_by(self):
        start = self.master_dripper.simulated_time
        self.master_dripper.update_by(dt.timedelta(minutes=25))
        self.assertEqual(start + dt.timedelta(minutes=25), self.master_dripper.simulated_time)
        for entry, time, serial_number in zip(Complete.objects.order_by('pk'),
                                              self.in_times,
                                              self.serial_numbers):
            assert(entry.serial_number == serial_number)
            assert(entry.completed == time)
        for entry, in_time, out_time, employee_number in zip(Attendance.objects.order_by('pk'),
                                                             self.in_times,
                                                             self.out_times,
                                                             self.employee_numbers):
            self.assertEqual(entry.employee_number, employee_number)
            self.assertEqual(entry.clock_in_time, in_time)
            if out_time is None or out_time > self.master_dripper.simulated_time:
                self.assertIsNone(entry.clock_out_time)
            else:
                self.assertEqual(entry.clock_out_time, out_time)

#class Test_Real_Data_Drippers(TestCase):
