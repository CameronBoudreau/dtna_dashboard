"""
Man hour calculation functions are in this file
"""

from get_data.models import EmpClockDataModel
import re
from django.utils import timezone
from .config.look_up_values import get_dept_lookup_dict


def get_clocked_in(start):
    """
    Filters employees who clocked in before shift time, excluding those who have clocked out from previous shifts
    :param start: datetime object the start of time that you want to look at
    :return: filtered objects before the start value
    """
    print('/*' * 50)
    print("GET CLOCKED IN")
    print('/*' * 50)
    with timezone.override("US/Eastern"):
        return EmpClockDataModel.objects.filter(
            CLOCK_IN_TIME__year=start.year,
            CLOCK_IN_TIME__month=start.month,
            CLOCK_IN_TIME__day=start.day,
            CLOCK_OUT_TIME__exact=None,
        ).exclude(
            CLOCK_OUT_REASON__exact='&out',
            CLOCK_IN_TIME__gte=start,
        )


def get_emp_who_left_during_shift(start, stop):
    """
    Filters employees who clocked out before the stop
    :param start: datetime object the start of time that you want to look at
    :param stop: datetime object the end of time that you want to look at
    :return: filtered objects within the start and stop range
    """

    with timezone.override("US/Eastern"):
        return EmpClockDataModel.objects.filter(
            CLOCK_IN_TIME__year=start.year,
            CLOCK_IN_TIME__month=start.month,
            CLOCK_IN_TIME__day=start.day,
            CLOCK_OUT_TIME__lte=stop,
            CLOCK_OUT_REASON__exact='&out',
        ).exclude(CLOCK_OUT_TIME__lte=start)


def get_emp_who_left_on_break(start, stop):
    """
    Filters employees who clocked out before the stop
    :param start: datetime object the start of time that you want to look at
    :param stop: datetime object the end of time that you want to look at
    :return: filtered objects within the start and stop range
    """

    with timezone.override("US/Eastern"):
        return EmpClockDataModel.objects.filter(
            CLOCK_IN_TIME__year=start.year,
            CLOCK_IN_TIME__month=start.month,
            CLOCK_IN_TIME__day=start.day,
            CLOCK_OUT_TIME__lte=stop,
            CLOCK_OUT_REASON__exact='&break',
        ).exclude(CLOCK_OUT_TIME__lte=start)


def get_emp_shift(dept_string):
    """
    Regex lookup command to find which shift the employee is in
    :param dept_string: expects a string from column EMP_DEPT_TXT that looks like '017.30000.00.51.05/1/-/017.P000051/-/-/-'
    :return: a string of shift containing shift number
    """
    try:
        print(dept_string)
        REGEX_FOR_DEPT = "/([1-9])/"
        regex_compiled = re.compile(REGEX_FOR_DEPT)
        shift = re.findall(regex_compiled, dept_string)[0]
    except IndexError:
        shift = '0'
    return shift


def get_emp_dept(dept_string):
    """
    Analyzes which department, plant, and shift that employee belongs too.
    :param dept_string: expects a string from column EMP_DEPT_TXT that looks like '017.30000.00.51.05/1/-/017.P000051/-/-/-'
    :return: emp_dept as string of 3 letter code, i.e. 'DEPT1'/'DEPT2'
    """

    emp_dept_code = dept_string[4:5]
    dept_lookup_dict = get_dept_lookup_dict()

    if emp_dept_code in dept_lookup_dict:
        emp_dept = dept_lookup_dict[emp_dept_code]
    else:
        emp_dept = 'OTHER'

    return emp_dept


def get_emp_plant_code(dept_string):
    """
    :param dept_string: expects a string from column EMP_DEPT_TXT that looks like '017.30000.00.51.05/1/-/017.P000051/-/-/-'
    :return: Returns string of plant code for employee
    """
    return dept_string[:3]


def get_emp_man_hours(employee, start, stop):
    """
    Calculates the employee's man hours from start to stop.
    :param employee: employee object
    :param start: DATETIME timezone aware object from the beginning of the snapshot
    :param stop: DATETIME timezone aware object from the ending of the snapshot
    :return: float of total employee mh
    """
    begin, end = set_begin_and_end_for_emp(employee, start, stop)
    emp_man_hours = ((end - begin).total_seconds()) / 3600
    return emp_man_hours


def set_begin_and_end_for_emp(employee, start, stop):
    """
    takes in the employee and computes when the begin and stop times for
     the employee should be as employees clock in and out before/during shifts
    :param employee: employee object
    :param start: DATETIME timezone aware object from the start
    :param stop: DATETIME timezone aware object from the ending
    :return: the begin and ending results as DATETIME timezone aware objects
    """
    # If before start, then capture start.
    begin = max(employee.CLOCK_IN_TIME, start)
    if employee.CLOCK_OUT_TIME:
        end = min(employee.CLOCK_OUT_TIME, stop)
    else:
        end = stop
    return begin, end


def get_employees(start, stop):
    """
    Gets employee queryset objects for currently clocked in,
    those who left, and those who went on break.
    :param start:  DATETIME TIMEZONE AWARE object
    :param stop:  DATETIME TIMEZONE AWARE object
    :return: one list of all employee objects that meet filter condition
    """

    currently_clocked_in = get_clocked_in(start)
    emp_that_left = get_emp_who_left_during_shift(start, stop)
    emp_that_break = get_emp_who_left_on_break(start, stop)

    return create_single_list_from_list_of_queryset([
        currently_clocked_in,
        emp_that_break,
        emp_that_left
    ])


def create_single_list_from_list_of_queryset(query_set_list):
    """
    Takes in query sets in a list and returns a list
    of all of the individual objects
    :param query_set_list: a list of multiple queryset objects
    :return: a single list of objects
    """
    master_list = []
    # takes the multiple query sets and returns one list.
    for query in query_set_list:
        for employee in query:
            master_list.append(employee)
    return master_list
