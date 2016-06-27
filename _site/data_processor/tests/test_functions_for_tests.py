from django.test import TestCase
from django.utils import timezone
import datetime as dt
from get_data.models import EmpClockDataModel
from .functions.functions_for_tests import find_pop_and_return, compare_expect_against_query
from data_processor.functions.man_hours_calculations import get_clocked_in


class FunctionsForTest(TestCase):
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

    def test_find_pop_and_return_expected(self):
        expected_employees = ['001', '004', '006']
        looking_for = '004'

        # testing items of the returned list
        found_item, returned_list = find_pop_and_return(
            looking_for=looking_for,
            expected_list=expected_employees,

        )

        # is what is found actually the item we are looking for?
        self.assertEqual(looking_for, found_item)

        # returned list should be 2 long
        self.assertEqual(len(returned_list), 2)

    def test_compare_expect_against_query(self):
        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        expected_employees = ['001', '004', '006', '005', '010']
        employees = get_clocked_in(start)
        print(employees)
        self.assertTrue(compare_expect_against_query(expected_employees, employees))

