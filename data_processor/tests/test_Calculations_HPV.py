from django.test import TestCase
from django.utils import timezone
import datetime as dt
from get_data.models import EmpClockDataModel
from data_processor.functions.hours_per_unit_calcuations import iterate_over_employees, calc_hours_per_unit
from data_processor.functions.man_hours_calculations import get_employees


class hours_per_unitCalculations(TestCase):
    @timezone.override("US/Eastern")
    def setUp(self):
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
            EMP_DEPT_TXT='017.10000.00.80.07/1/-/017.P000080/-/-/-',
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
            EMP_DEPT_TXT='017.30000.00.80.07/1/-/017.P000080/-/-/-',
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
            EMP_DEPT_TXT='017.30000.00.80.07/1/-/017.P000080/-/-/-',
            CLOCK_IN_REASON='&newShift',
            CLOCK_IN_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 39)),
            CLOCK_OUT_REASON='&break',
            CLOCK_OUT_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 8, 30)),
        )

        EmpClockDataModel.objects.create(
            EMP_ID_TXT='010',
            EMP_NAME='Janet',
            EMP_DEPT_TXT='017.30000.00.80.07/1/-/017.P000080/-/-/-',
            CLOCK_IN_REASON='&newShift',
            CLOCK_IN_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 9, 30)),
            CLOCK_OUT_REASON='&missedOut',
            CLOCK_OUT_TIME=None,
        )

    @timezone.override("US/Eastern")
    def test_iterate_over_employees(self):
        test_dept_dict = {
            'DEPT1': {
                'mh': 0,
                'ne': 0,
                'hours_per_unit': 0,
            },
            'DEPT2': {
                'mh': 0,
                'ne': 0,
                'hours_per_unit': 0,
            },
            'DEPT3': {
                'mh': 0,
                'ne': 0,
                'hours_per_unit': 0,
            },
            'PLANT': {
                'mh': 0,
                'ne': 0,
                'hours_per_unit': 0,
            },
            'claims_for_range': 10
        }

        expected_dict = {
            'PLANT': {
                'ne': 7,
                'hours_per_unit': 2.095,
                'mh': 20.950000000000003
            },
            'DEPT2': {
                'ne': 2,
                'hours_per_unit': 0.8,
                'mh': 8.0
            },
            'DEPT3': {
                'ne': 4,
                'hours_per_unit': 0.8949999999999999,
                'mh': 8.95
            },
            'DEPT1': {
                'ne': 1,
                'hours_per_unit': 0.4,
                'mh': 4.0
            },
            'claims_for_range': 10
        }

        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        stop = timezone.make_aware(dt.datetime(2016, 6, 3, 10, 30))
        employees = get_employees(start, stop)
        result_dict = iterate_over_employees(test_dept_dict, employees, start, stop)
        print(result_dict)
        for key in result_dict:
            if key != 'claims_for_range':
                self.assertEqual(
                    result_dict[key]['hours_per_unit'],
                    expected_dict[key]['hours_per_unit']
                )
                self.assertEqual(
                    result_dict[key]['ne'],
                    expected_dict[key]['ne']
                )
                self.assertEqual(
                    result_dict[key]['mh'],
                    expected_dict[key]['mh']
                )

    def test_calc_hours_per_unit(self):
        claims = 5
        test_dept_dict = {
            'mh': 30,
            'ne': 10,
            'hours_per_unit': 0,
        }

        plant_dict = {
            'ne': 10,
            'hours_per_unit': 0,
            'mh': 20,
        }

        dept_result, plant_result = calc_hours_per_unit(claims, test_dept_dict, plant_dict)
        self.assertEqual(dept_result['hours_per_unit'], 6)
        self.assertEqual(plant_result['hours_per_unit'], 4)

