import random
from datetime import datetime


def get_employee():
    return random.randint(60000, 89999)


def clock_in(day, hour):
    minute = random.randint(0, 29)
    clock = datetime(2016, 6, day, hour, minute)
    return clock


def clock_out(day, hour):
    clock = datetime(2016, 6, day, hour + 9, 0)
    return clock


def get_dept():
    return random.choice(['DEPT1', 'DEPT2', 'DEPT4', 'DEPT5', 'DEPT3'])


def get_truck_serial():
    serial = random.choice(['HX', 'HY', 'HV', 'JB']) + str(random.randint(3201, 8900))
    return serial


def get_completed(day, hour, minute):
    clock = datetime(2016, 6, day, hour, minute)
    return clock
