"""
Testing the manhours calucaltion functions.
Each class is a building up the test case.
"""

from django.test import TestCase
from django.utils import timezone
import datetime as dt

from data_processor.tests.functions.functions_for_tests import find_pop_and_return
from get_data.models import EmpClockDataModel

from data_processor.functions.man_hours_calculations import get_clocked_in
from data_processor.functions.man_hours_calculations import get_emp_man_hours, get_emp_dept
from data_processor.functions.man_hours_calculations import get_emp_who_left_during_shift
from data_processor.functions.man_hours_calculations import set_begin_and_end_for_emp
from data_processor.functions.man_hours_calculations import get_emp_who_left_on_break
from data_processor.functions.man_hours_calculations import get_emp_shift
from data_processor.functions.man_hours_calculations import get_emp_plant_code
from data_processor.functions.man_hours_calculations import create_single_list_from_list_of_queryset

from data_processor.functions.hours_per_unit_calcuations import iterate_over_employees

from data_processor.functions.config.look_up_values import get_master_by_dept_dict

from data_processor.functions.process_data_main import get_employees

from data_processor.tests.functions.functions_for_tests import compare_expect_against_query


class ManHourEdgeTestCaseClockedOutEarly(TestCase):
    """
    Test to see if people are clocked in and man hours are tracked
    for those and others that clocked out during the shift.
    """

    @timezone.override("US/Eastern")
    def setUp(self):
        #################################################
        # Previous Day Clock In/Out
        #################################################
        EmpClockDataModel.objects.create(
            EMP_ID_TXT='001',
            EMP_NAME='Cameron',
            EMP_DEPT_TXT='017.30000.00.51.05/1/-/017.P000051/-/-/-',
            CLOCK_IN_REASON='&newShift',
            CLOCK_IN_TIME=timezone.make_aware(dt.datetime(2016, 6, 2, 5, 35)),
            CLOCK_OUT_REASON='&out',
            CLOCK_OUT_TIME=timezone.make_aware(dt.datetime(2016, 6, 2, 14, 32)),
        )

        EmpClockDataModel.objects.create(
            EMP_ID_TXT='002',
            EMP_NAME='Nic',
            EMP_DEPT_TXT='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            CLOCK_IN_REASON='&newShift',
            CLOCK_IN_TIME=timezone.make_aware(dt.datetime(2016, 6, 2, 22, 29)),
            CLOCK_OUT_REASON='&out',
            CLOCK_OUT_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 32)),
        )
        #################################################
        # Previous Day Forgot Clock Out
        #################################################
        EmpClockDataModel.objects.create(
            EMP_ID_TXT='001',
            EMP_NAME='Cameron',
            EMP_DEPT_TXT='017.30000.00.51.05/1/-/017.P000051/-/-/-',
            CLOCK_IN_REASON='&newShift',
            CLOCK_IN_TIME=timezone.make_aware(dt.datetime(2016, 6, 2, 5, 35)),
            CLOCK_OUT_REASON='&missedOut',
            CLOCK_OUT_TIME=None
        )

        #################################################
        # Clock In
        #################################################
        EmpClockDataModel.objects.create(
            EMP_ID_TXT='001',
            EMP_NAME='Cameron',
            EMP_DEPT_TXT='017.30000.00.51.05/1/-/017.P000051/-/-/-',
            CLOCK_IN_REASON='&newShift',
            CLOCK_IN_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 5, 35)),
            CLOCK_OUT_REASON='&missedOut',
            CLOCK_OUT_TIME=None
        )

        EmpClockDataModel.objects.create(
            EMP_ID_TXT='006',
            EMP_NAME='Alex',
            EMP_DEPT_TXT='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            CLOCK_IN_REASON='&newShift',
            CLOCK_IN_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 19)),
            CLOCK_OUT_REASON='&missedOut',
            CLOCK_OUT_TIME=None
        )

        EmpClockDataModel.objects.create(
            EMP_ID_TXT='004',
            EMP_NAME='Stacey',
            EMP_DEPT_TXT='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            CLOCK_IN_REASON='&newShift',
            CLOCK_IN_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 25)),
            CLOCK_OUT_REASON='missedOut',
            CLOCK_OUT_TIME=None,
        )

        #################################################
        # Employees late
        #################################################
        EmpClockDataModel.objects.create(
            EMP_ID_TXT='005',
            EMP_NAME='Stacey',
            EMP_DEPT_TXT='017.20000.00.80.07/1/-/017.P000080/-/-/-',
            CLOCK_IN_REASON='&newShift',
            CLOCK_IN_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30)),
            CLOCK_OUT_REASON='&missedOut',
            CLOCK_OUT_TIME=None
        )

        #################################################
        # Employees left early
        #################################################
        EmpClockDataModel.objects.create(
            EMP_ID_TXT='002',
            EMP_NAME='Nic',
            EMP_DEPT_TXT='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            CLOCK_IN_REASON='&newShift',
            CLOCK_IN_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 45)),
            CLOCK_OUT_REASON='&out',
            CLOCK_OUT_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 8, 51)),
        )

        ################################################
        # Employees left early and then came back
        ################################################
        EmpClockDataModel.objects.create(
            EMP_ID_TXT='010',
            EMP_NAME='Janet',
            EMP_DEPT_TXT='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            CLOCK_IN_REASON='&newShift',
            CLOCK_IN_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 39)),
            CLOCK_OUT_REASON='&break',
            CLOCK_OUT_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 8, 30)),
        )

        EmpClockDataModel.objects.create(
            EMP_ID_TXT='010',
            EMP_NAME='Janet',
            EMP_DEPT_TXT='017.80000.00.80.07/1/-/017.P000080/-/-/-',
            CLOCK_IN_REASON='&newShift',
            CLOCK_IN_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 9, 30)),
            CLOCK_OUT_REASON='&missedOut',
            CLOCK_OUT_TIME=None,
        )

    #################################################
    # Tests
    #################################################

    @timezone.override("US/Eastern")
    def test_get_clocked_in(self):
        """Test for employees who clocked in is accurate"""
        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        expected_employees = ['001', '004', '006', '005', '010']
        neg_counter = len(expected_employees)

        # test that expected employees is what is found
        employees = get_clocked_in(start)
        for employee in employees:
            print(employee.EMP_ID_TXT)
            print(expected_employees)

            # testing that the length of expected goes to 0 and that we are not missing things
            self.assertEqual(len(expected_employees), neg_counter)
            neg_counter -= 1

            found_item, expected_employees = find_pop_and_return(
                looking_for=employee.EMP_ID_TXT,
                expected_list=expected_employees,
            )
            self.assertEqual(employee.EMP_ID_TXT, found_item)

    @timezone.override("US/Eastern")
    def test_get_emp_who_left_during_shift(self):
        """Test for employees who clocked in before start is accurate"""
        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        stop = timezone.make_aware(dt.datetime(2016, 6, 3, 10, 30))
        expected_employees = ['002']
        neg_counter = len(expected_employees)

        # test that expected employees is what is found
        employees = get_emp_who_left_during_shift(
            start=start,
            stop=stop,
        )

        for employee in employees:
            print(employee.EMP_ID_TXT)
            print(expected_employees)

            # testing that the length of expected goes to 0 and that we are not missing things
            self.assertEqual(len(expected_employees), neg_counter)
            neg_counter -= 1

            found_item, expected_employees = find_pop_and_return(
                looking_for=employee.EMP_ID_TXT,
                expected_list=expected_employees,
            )
            self.assertEqual(employee.EMP_ID_TXT, found_item)

    @timezone.override("US/Eastern")
    def test_get_emp_who_left_on_break(self):
        """Test for employees who clocked in before start is accurate"""
        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        stop = timezone.make_aware(dt.datetime(2016, 6, 3, 10, 30))
        expected_employees = ['010']
        neg_counter = len(expected_employees)

        # test that expected employees is what is found
        employees = get_emp_who_left_on_break(
            start=start,
            stop=stop,
        )

        for employee in employees:
            print("BREAK!!!")
            print(employee.EMP_ID_TXT)
            print(expected_employees)

            # testing that the length of expected goes to 0 and that we are not missing things
            self.assertEqual(len(expected_employees), neg_counter)
            neg_counter -= 1

            found_item, expected_employees = find_pop_and_return(
                looking_for=employee.EMP_ID_TXT,
                expected_list=expected_employees,
            )
            self.assertEqual(employee.EMP_ID_TXT, found_item)

    def test_get_emp_shift(self):
        employee_dept_test_list = [
            '017.30000.00.51.05/1/-/017.P000051/-/-/-',
            '017.90000.00.00.21/2/-/017.I996063/-/-/-',
            '017.60000.00.84.43/2/-/017.P000085/-/-/-',
            '017.20000.00.84.01/1/-/017.P000084/-/-/-',
            '017.80000.00.80.09/3/-/017.P000080/-/-/-',
            '017.10000.00.00.12/1/-/017.I996063/-/-/-',
            'asdasdafasdfasd',
            '017.10000.00.00.12//-/017.I996063/-/-/-',
        ]
        expected_shift_list = ['1', '2', '2', '1', '3', '1', '0']

        for employee, expected in zip(employee_dept_test_list, expected_shift_list):
            self.assertEqual(get_emp_shift(employee), expected)

    def test_process_department_string(self):
        """Testing base functionality of process department to make sure that we are ripping the correct data out"""
        employee_dept_test_list = [
            '017.30000.00.51.05/1/-/017.P000051/-/-/-',
            '017.90000.00.00.21/2/-/017.I996063/-/-/-',
            '017.60000.00.84.43/2/-/017.P000085/-/-/-',
            '017.20000.00.84.01/1/-/017.P000084/-/-/-',
            '017.80000.00.80.09/3/-/017.P000080/-/-/-',
            '017.10000.00.00.12/1/-/017.I996063/-/-/-'
        ]

        expected_dept_test_list = ['DEPT3', 'DEPT9', 'DEPT6', 'DEPT2', 'DEPT8', 'DEPT1']

        for index, item in enumerate(employee_dept_test_list):
            # print("/"*50)
            # print('index = ', index)
            # print('item = ', item)
            emp_dept = get_emp_dept(item)
            self.assertEqual(expected_dept_test_list[index], emp_dept)

    def test_emp_plant_code(self):
        employee_dept_test_list = [
            '017.30000.00.51.05/1/-/017.P000051/-/-/-',
            '017.90000.00.00.21/2/-/017.I996063/-/-/-',
            '013.60000.00.84.43/2/-/017.P000085/-/-/-',
            '017.20000.00.84.01/1/-/017.P000084/-/-/-',
            '017.80000.00.80.09/3/-/017.P000080/-/-/-',
            '016.10000.00.00.12/1/-/017.I996063/-/-/-'
        ]
        expected_plant_list = ['017', '017', '013', '017', '017', '016', ]
        for employee, expected in zip(employee_dept_test_list, expected_plant_list):
            self.assertEqual(get_emp_plant_code(employee), expected)

    @staticmethod
    def get_expected_dictionary():
        return {'DEPT3': {'mh': 3.15, 'hours_per_unit': 3.15, 'ne': 1}, 'PLANT': {'mh': 16.7, 'hours_per_unit': 16.7, 'ne': 7},
                'DEPT2': {'mh': 6.3, 'hours_per_unit': 6.3, 'ne': 2}, 'claims_for_range': 1, 'OTHER': {'mh': 0, 'hours_per_unit': 0, 'ne': 0},
                'DEPT1': {'mh': 0, 'hours_per_unit': 0, 'ne': 0}, 'DEPT9': {'mh': 0, 'hours_per_unit': 0, 'ne': 0},
                'DEPT7': {'mh': 0, 'hours_per_unit': 0, 'ne': 0}, 'DEPT6': {'mh': 0, 'hours_per_unit': 0, 'ne': 0},
                'DEPT5': {'mh': 0, 'hours_per_unit': 0, 'ne': 0}, 'DEPT4': {'mh': 0, 'hours_per_unit': 0, 'ne': 0},
                'DEPT8': {'mh': 7.25, 'hours_per_unit': 7.25, 'ne': 4}}

    def test_get_master_by_dept_dict(self):
        dict_master = get_master_by_dept_dict()
        for key in dict_master:
            if key == 'claims_for_range':
                self.assertEqual(dict_master[key], 0)
            else:
                for subkey in dict_master[key]:
                    self.assertEqual(dict_master[key][subkey], 0)

    @timezone.override("US/Eastern")
    def test_emp_man_hours(self):
        """Test for employees who clocked in before start is accurate"""
        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        stop = timezone.make_aware(dt.datetime(2016, 6, 3, 10, 30))
        emp_hours = 0

        expected_emp_hours = 20.95

        # getting employee objects that are clocked in
        clocked_in_emp = get_clocked_in(start)
        emp_that_left = get_emp_who_left_during_shift(start, stop)
        emp_that_breaked = get_emp_who_left_on_break(start, stop)

        # testing return of number of hours
        for employee in clocked_in_emp:
            print("EMP= ", employee.EMP_ID_TXT)
            emp_hour = get_emp_man_hours(employee, start, stop)
            print("EMP HOUR= ", emp_hour)
            emp_hours += emp_hour

        for employee in emp_that_left:
            print("EMP= ", employee.EMP_ID_TXT)
            emp_hour = get_emp_man_hours(employee, start, stop)
            print("EMP HOUR= ", emp_hour)
            emp_hours += emp_hour

        for employee in emp_that_breaked:
            print("EMP= ", employee.EMP_ID_TXT)
            emp_hour = get_emp_man_hours(employee, start, stop)
            print("EMP HOUR= ", emp_hour)
            emp_hours += emp_hour

        self.assertAlmostEqual(emp_hours, expected_emp_hours)

    @timezone.override("US/Eastern")
    def test_set_begin_and_end_for_emp(self):
        """
        Test to make sure the the set being and end for emp is returning the values requested
        """
        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        stop = timezone.make_aware(dt.datetime(2016, 6, 3, 10, 30))
        expected_begin = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        expected_end = timezone.make_aware(dt.datetime(2016, 6, 2, 14, 32))

        example_employee = EmpClockDataModel.objects.first()
        begin, end = set_begin_and_end_for_emp(
            employee=example_employee,
            start=start,
            stop=stop,
        )

        self.assertEqual(expected_begin, begin)
        self.assertEqual(expected_end, end)

    @timezone.override("US/Eastern")
    def test_get_employees(self):
        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        stop = timezone.make_aware(dt.datetime(2016, 6, 3, 9, 39))
        expected_employees = ['001', '004', '006', '005', '010', '010', '002']

        results_list = get_employees(start, stop)

        self.assertTrue(compare_expect_against_query(expected_employees, results_list))

    @timezone.override("US/Eastern")
    def test_iterate_over_employees(self):
        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        stop = timezone.make_aware(dt.datetime(2016, 6, 3, 9, 39))
        expected_employees = ['001', '004', '006', '005', '010']
        dept_dict = get_master_by_dept_dict()
        dept_dict['claims_for_range'] = 1

        expected_dict = ManHourEdgeTestCaseClockedOutEarly.get_expected_dictionary()
        employees = get_employees(start, stop)

        self.assertTrue(compare_expect_against_query(expected_employees, employees))

        dept_dict = iterate_over_employees(dept_dict, employees, start, stop)

        print(dept_dict)
        print(expected_dict)
        self.assertEqual(expected_dict, dept_dict)

    @timezone.override("US/Eastern")
    def test_create_single_list_from_list_of_queryset(self):
        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        stop = timezone.make_aware(dt.datetime(2016, 6, 3, 9, 39))

        # can't call get_employees because that function uses create single list
        currently_clocked_in = get_clocked_in(start)
        emp_that_left = get_emp_who_left_during_shift(start, stop)
        emp_that_break = get_emp_who_left_on_break(start, stop)

        expected_employees = ['001', '004', '006', '005', '010']

        result_list = create_single_list_from_list_of_queryset([
            currently_clocked_in,
            emp_that_break,
            emp_that_left
        ])

        self.assertTrue(compare_expect_against_query(expected_employees, result_list))



