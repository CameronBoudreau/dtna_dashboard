from django.test import TestCase
from django.utils import timezone
import datetime as dt

from data_processor.functions.process_data_main import get_master_by_dept_dict
from data_processor.functions.process_data_main import get_employees
from get_data.models import EmpClockDataModel
from data_processor.tests.functions.functions_for_tests import compare_expect_against_query
from data_processor.functions.hours_per_unit_calcuations import iterate_over_employees


class Calculations_Main(TestCase):
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




    # def test_verify_datetime_object(self):
    #     expected_results = [True, False, False, None]
    #     # timezone aware
    #     test1 = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
    #     # not timezone aware
    #     test2 = dt.datetime(2016, 6, 3, 6, 30).replace(tzinfo=None)
    #     # not a DT object
    #     test3 = '2016, 6, 3, 6, 30'
    #     # a None test
    #     test4 = None
    #
    #     results = verify_aware_datetime_object([test1, test2, test3, test4])
    #     for result, expected in zip(results, expected_results):
    #         self.assertEqual(result, expected)
