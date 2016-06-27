from django.test import TestCase
from django.utils import timezone
from get_data.models import PlantActivityModel
from plantsettings.models import PlantSetting
from api.models import hours_per_unitATM
import data_processor.tests.test_files.hours_per_unit_dict_test_cases as tc
import data_processor.tests.test_files.api_test_cases as api_tc
import data_processor.tests.test_files.plant_settings_test_cases as ps_tc

import datetime as dt

from data_processor.processor_functions.processor_get_new_hours_per_unit import get_new_hours_per_unit_data

from data_processor.processor_functions.processor_day_hours_per_unit import get_day_hours_per_unit_dict

from data_processor.processor_functions.processor_delete_old import delete_old_entries

from data_processor.processor_functions.processor_dept_day_stats import get_dept_day_stats

from data_processor.processor_functions.processor_plant_day_stats import get_plant_day_hours_per_unit

from data_processor.processor_functions.processor_shift import get_shift_info, get_day_start

from data_processor.processor_functions.processor_write_conditions import need_to_write

class Gethours_per_unitData(TestCase):
    def setUp(self):
        PlantActivityModel.objects.create(
            UNIT_NUM='HZ3852',
            UNIT_COMPLETED_DEPT='03',
            UNIT_LOADED_TIME=timezone.make_aware(dt.datetime(2016, 6, 2, 6, 55)),
        )

        # timestamp after last write, but wrong pool number for false-positives
        PlantActivityModel.objects.create(
            UNIT_NUM='HZ3853',
            UNIT_COMPLETED_DEPT='01',
            UNIT_LOADED_TIME=timezone.make_aware(dt.datetime(2016, 6, 2, 19, 55)),
        )

    def test_get_new_hours_per_unit_data_no_new_claims_recent_entry(self):
        hours_per_unitATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_7_am)
        PlantSetting.objects.create(**ps_tc.default_plant_settings_7_05)

        self.assertEqual(get_new_hours_per_unit_data(), None)

    def test_get_new_hours_per_unit_data_no_new_claims_15_min_since_write(self):
        # API 6/2 @ 7:00
        hours_per_unitATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_7_am)
        # Now/Plant 6/2 @ 8:00
        PlantSetting.objects.create(**ps_tc.three_shift_8_am_plant_settings)

        self.assertEqual(get_new_hours_per_unit_data(), True)

    def test_get_new_hours_per_unit_data_no_new_claims_end_shift_recent_entry(self):
        # API 6/2 @ 14:25
        hours_per_unitATM.objects.create(**api_tc.two_shifts_first_shift_api_entry)
        # Now/Plant 6/2 @ 14:27
        PlantSetting.objects.create(**ps_tc.default_plant_settings_14_27)

        self.assertEqual(get_new_hours_per_unit_data(), True)

    def test_get_new_hours_per_unit_data_no_api_entries(self):
        PlantSetting.objects.create(**ps_tc.three_shift_8_am_plant_settings)

        self.assertEqual(get_new_hours_per_unit_data(), True)

    def test_get_new_hours_per_unit_data_no_claims(self):
        PlantActivityModel.objects.all().delete()
        PlantSetting.objects.create(**ps_tc.default_plant_settings_7_05)

        self.assertEqual(get_new_hours_per_unit_data(), None)


class GetShiftInfoThreeShifts(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.three_shift_8_am_plant_settings)

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_early_3rd_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 3, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 1, 22, 30))
        expected_shift = 3

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_1st_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 8, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 6, 30))
        expected_shift = 1

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_2nd_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 14, 30))
        expected_shift = 2

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_late_3rd_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 23, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 22, 30))
        expected_shift = 3

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))


class GetShiftInfoTwoShifts(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.two_shift_8_am_plant_settings)

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_OT_1st_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 3, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 0, 0))
        expected_shift = 1

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_OT_2nd_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 2, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 1, 14, 30))
        expected_shift = 2

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_1st_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 8, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 6, 30))
        expected_shift = 1

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_2nd_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 14, 30))
        expected_shift = 2

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))


class GetShiftInfoOneShift(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.one_shift_8_am_plant_settings)

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_before_first_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 1, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 0, 0))
        expected_shift = 1

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_1st_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 8, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 6, 30))
        expected_shift = 1

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))

    @timezone.override("US/Eastern")
    def test_get_shift_info_now_evening(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 18, 0))
        settings = PlantSetting.objects.latest('timestamp')
        expected_start = timezone.make_aware(dt.datetime(2016, 6, 2, 6, 30))
        expected_shift = 1

        self.assertEqual(get_shift_info(settings, now),
                         (expected_start, expected_shift))


class GetDayStart(TestCase):
    def test_get_day_start_three_shifts_day_of(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 1, 23, 30))
        PlantSetting.objects.create(**ps_tc.three_shift_8_am_plant_settings)
        settings = PlantSetting.objects.latest('timestamp')
        expected_day_start = timezone.make_aware(dt.datetime(2016, 6, 1, 22, 30))

        self.assertEqual(get_day_start(settings, now), expected_day_start)

    def test_get_day_start_three_shifts_day_after(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 12, 0))
        PlantSetting.objects.create(**ps_tc.three_shift_8_am_plant_settings)
        settings = PlantSetting.objects.latest('timestamp')
        expected_day_start = timezone.make_aware(dt.datetime(2016, 6, 1, 22, 30))

        self.assertEqual(get_day_start(settings, now), expected_day_start)

    def test_get_day_start_less_than_three_shifts(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 12, 0))
        PlantSetting.objects.create(**ps_tc.two_shift_8_am_plant_settings)
        settings = PlantSetting.objects.latest('timestamp')
        expected_day_start = timezone.make_aware(dt.datetime(2016, 6, 2, 6, 30))

        self.assertEqual(get_day_start(settings, now), expected_day_start)


class GetDayStatsThreeShiftsPlant(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.three_shift_8_am_plant_settings)

    def test_get_plant_day_hours_per_unit_third_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 1, 23, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_3_hours_per_unit_dict_with_plant

        expected_hours_per_unit = 90
        expected_working_hours = 90
        expected_claims = 1

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_third_shift_0_hours_per_unit(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 1, 23, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_3_hours_per_unit_dict_with_plant_0_hours_per_unit

        expected_hours_per_unit = 0
        expected_working_hours = 0
        expected_claims = 0

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_first_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_1_hours_per_unit_dict_with_plant
        hours_per_unitATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)

        expected_hours_per_unit = 90
        expected_working_hours = 810
        expected_claims = 9

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_first_shift_0_hours_per_unit(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_1_hours_per_unit_dict_with_plant_0_hours_per_unit
        hours_per_unitATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)

        expected_hours_per_unit = 90
        expected_working_hours = 720
        expected_claims = 8

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_first_shift_0_claims(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_1_hours_per_unit_dict_with_plant_0_hours_per_unit
        hours_per_unitATM.objects.create(**api_tc.three_shifts_third_shift_api_entry_0_claims)

        expected_hours_per_unit = 0
        expected_working_hours = 720
        expected_claims = 0

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_first_shift_no_api_entries(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_1_hours_per_unit_dict_with_plant

        expected_hours_per_unit = 90
        expected_working_hours = 90
        expected_claims = 1

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_second_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict_with_plant
        hours_per_unitATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)
        hours_per_unitATM.objects.create(**api_tc.three_shifts_first_shift_api_entry)

        expected_hours_per_unit = 90
        expected_working_hours = 1530
        expected_claims = 17

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_second_shift_0_hours_per_unit(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict_with_plant_0_hours_per_unit
        hours_per_unitATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)
        hours_per_unitATM.objects.create(**api_tc.three_shifts_first_shift_api_entry)

        expected_hours_per_unit = 90
        expected_working_hours = 1440
        expected_claims = 16

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_second_shift_0_claims(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict_with_plant_0_hours_per_unit
        hours_per_unitATM.objects.create(**api_tc.three_shifts_third_shift_api_entry_0_claims)
        hours_per_unitATM.objects.create(**api_tc.three_shifts_first_shift_api_entry_0_claims)

        expected_hours_per_unit = 0
        expected_working_hours = 1440
        expected_claims = 0

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_second_shift_no_third_shift_api_entry(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict_with_plant
        hours_per_unitATM.objects.create(**api_tc.three_shifts_first_shift_api_entry)

        expected_hours_per_unit = 90
        expected_working_hours = 810
        expected_claims = 9

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_second_shift_no_first_shift_api_entry(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict_with_plant
        hours_per_unitATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)

        expected_hours_per_unit = 90
        expected_working_hours = 810
        expected_claims = 9

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_second_shift_no_api_entries(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict_with_plant

        expected_hours_per_unit = 90
        expected_working_hours = 90
        expected_claims = 1

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                        (expected_hours_per_unit, expected_working_hours, expected_claims))


class GetDayStatsTwoShiftsPlant(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.two_shift_8_am_plant_settings)

    def test_get_plant_day_hours_per_unit_first_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_1_hours_per_unit_dict_with_plant

        expected_hours_per_unit = 90
        expected_working_hours = 90
        expected_claims = 1

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_first_shift_0_hours_per_unit(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_1_hours_per_unit_dict_with_plant_0_hours_per_unit

        expected_hours_per_unit = 0
        expected_working_hours = 0
        expected_claims = 0

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_second_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict_with_plant
        hours_per_unitATM.objects.create(**api_tc.two_shifts_first_shift_api_entry)

        expected_hours_per_unit = 90
        expected_working_hours = 810
        expected_claims = 9

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_second_shift_0_hours_per_unit(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict_with_plant_0_hours_per_unit
        hours_per_unitATM.objects.create(**api_tc.two_shifts_first_shift_api_entry)

        expected_hours_per_unit = 90
        expected_working_hours = 720
        expected_claims = 8

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_second_shift_0_claims(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict_with_plant_0_hours_per_unit
        hours_per_unitATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_0_claims)

        expected_hours_per_unit = 0
        expected_working_hours = 720
        expected_claims = 0

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_second_shift_no_first_shift_api_entry(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict_with_plant

        expected_hours_per_unit = 90
        expected_working_hours = 90
        expected_claims = 1

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))


class GetDayStatsOneShiftPlant(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.one_shift_8_am_plant_settings)

    def test_get_plant_day_hours_per_unit_first_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_1_hours_per_unit_dict_with_plant

        expected_hours_per_unit = 90
        expected_working_hours = 90
        expected_claims = 1

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))

    def test_get_plant_day_hours_per_unit_first_shift_0_hours_per_unit(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_1_hours_per_unit_dict_with_plant_0_hours_per_unit

        expected_hours_per_unit = 0
        expected_working_hours = 0
        expected_claims = 0

        self.assertEqual(get_plant_day_hours_per_unit(hours_per_unit_dict, now),
                         (expected_hours_per_unit, expected_working_hours, expected_claims))


class GetDayStatsThreeShiftsDept(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.three_shift_8_am_plant_settings)

    def test_get_dept_day_stats_third_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 1, 23, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_3_hours_per_unit_dict
        dept_list = ['DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8', 'DEPT9', 'OTHER']

        expected_hours_per_unit = 10
        expected_working_hours = 10

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hours_per_unit = 0
                expected_working_hours = 0
            self.assertEqual(get_dept_day_stats(hours_per_unit_dict, now, dept),
                             (expected_hours_per_unit, expected_working_hours))

    def test_get_dept_day_stats_first_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_1_hours_per_unit_dict
        hours_per_unitATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)

        dept_list = ['DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8', 'DEPT9', 'OTHER']

        expected_hours_per_unit = 10
        expected_working_hours = 90

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hours_per_unit = 0
                expected_working_hours = 0
            self.assertEqual(get_dept_day_stats(hours_per_unit_dict, now, dept),
                             (expected_hours_per_unit, expected_working_hours))

    def test_get_dept_day_stats_first_shift_0_claims(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_1_hours_per_unit_dict_0_hours_per_unit
        hours_per_unitATM.objects.create(**api_tc.three_shifts_third_shift_api_entry_0_claims)

        dept_list = ['DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8', 'DEPT9', 'OTHER']

        expected_hours_per_unit = 0
        expected_working_hours = 80

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hours_per_unit = 0
                expected_working_hours = 0
            self.assertEqual(get_dept_day_stats(hours_per_unit_dict, now, dept),
                             (expected_hours_per_unit, expected_working_hours))

    def test_get_dept_day_stats_first_shift_no_third_shift_api_entry(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_1_hours_per_unit_dict

        dept_list = ['DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8', 'DEPT9', 'OTHER']

        expected_hours_per_unit = 10
        expected_working_hours = 10

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hours_per_unit = 0
                expected_working_hours = 0
            self.assertEqual(get_dept_day_stats(hours_per_unit_dict, now, dept),
                             (expected_hours_per_unit, expected_working_hours))

    def test_get_dept_day_stats_second_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict
        hours_per_unitATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)
        hours_per_unitATM.objects.create(**api_tc.three_shifts_first_shift_api_entry)

        dept_list = ['DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8', 'DEPT9', 'OTHER']

        expected_hours_per_unit = 10
        expected_working_hours = 170

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hours_per_unit = 0
                expected_working_hours = 0
            self.assertEqual(get_dept_day_stats(hours_per_unit_dict, now, dept),
                             (expected_hours_per_unit, expected_working_hours))

    def test_get_dept_day_stats_second_shift_0_claims(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict_0_hours_per_unit
        hours_per_unitATM.objects.create(**api_tc.three_shifts_third_shift_api_entry_0_claims)
        hours_per_unitATM.objects.create(**api_tc.three_shifts_first_shift_api_entry_0_claims)

        dept_list = ['DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8', 'DEPT9', 'OTHER']

        expected_hours_per_unit = 0
        expected_working_hours = 160

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hours_per_unit = 0
                expected_working_hours = 0
            self.assertEqual(get_dept_day_stats(hours_per_unit_dict, now, dept),
                             (expected_hours_per_unit, expected_working_hours))

    def test_get_dept_day_stats_second_shift_no_api_entries(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict

        dept_list = ['DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8', 'DEPT9', 'OTHER']

        expected_hours_per_unit = 10
        expected_working_hours = 10

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hours_per_unit = 0
                expected_working_hours = 0
            self.assertEqual(get_dept_day_stats(hours_per_unit_dict, now, dept),
                             (expected_hours_per_unit, expected_working_hours))

    def test_get_dept_day_stats_second_shift_no_third_shift_api_entry(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict
        hours_per_unitATM.objects.create(**api_tc.three_shifts_first_shift_api_entry)

        dept_list = ['DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8', 'DEPT9', 'OTHER']

        expected_hours_per_unit = 10
        expected_working_hours = 90

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hours_per_unit = 0
                expected_working_hours = 0
            self.assertEqual(get_dept_day_stats(hours_per_unit_dict, now, dept),
                             (expected_hours_per_unit, expected_working_hours))

    def test_get_dept_day_stats_second_shift_no_first_shift_api_entry(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict
        hours_per_unitATM.objects.create(**api_tc.three_shifts_third_shift_api_entry)

        dept_list = ['DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8', 'DEPT9', 'OTHER']

        expected_hours_per_unit = 10
        expected_working_hours = 90

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hours_per_unit = 0
                expected_working_hours = 0
            self.assertEqual(get_dept_day_stats(hours_per_unit_dict, now, dept),
                             (expected_hours_per_unit, expected_working_hours))


class GetDayStatsTwoShiftsDept(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.two_shift_8_am_plant_settings)

    def test_get_dept_day_stats_first_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_1_hours_per_unit_dict
        dept_list = ['DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8', 'DEPT9', 'OTHER']

        expected_hours_per_unit = 10
        expected_working_hours = 10

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hours_per_unit = 0
                expected_working_hours = 0
            self.assertEqual(get_dept_day_stats(hours_per_unit_dict, now, dept),
                             (expected_hours_per_unit, expected_working_hours))

    def test_get_dept_day_stats_second_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict
        hours_per_unitATM.objects.create(**api_tc.two_shifts_first_shift_api_entry)
        dept_list = ['DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8', 'DEPT9', 'OTHER']

        expected_hours_per_unit = 10
        expected_working_hours = 90

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hours_per_unit = 0
                expected_working_hours = 0
            self.assertEqual(get_dept_day_stats(hours_per_unit_dict, now, dept),
                             (expected_hours_per_unit, expected_working_hours))

    def test_get_dept_day_stats_second_shift_0_claims(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict_0_hours_per_unit
        hours_per_unitATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_0_claims)
        dept_list = ['DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8', 'DEPT9', 'OTHER']

        expected_hours_per_unit = 0
        expected_working_hours = 80

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hours_per_unit = 0
                expected_working_hours = 0
            self.assertEqual(get_dept_day_stats(hours_per_unit_dict, now, dept),
                             (expected_hours_per_unit, expected_working_hours))

    def test_get_dept_day_stats_second_shift_no_api_entries(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict
        dept_list = ['DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8', 'DEPT9', 'OTHER']

        expected_hours_per_unit = 10
        expected_working_hours = 10

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hours_per_unit = 0
                expected_working_hours = 0
            self.assertEqual(get_dept_day_stats(hours_per_unit_dict, now, dept),
                             (expected_hours_per_unit, expected_working_hours))


class GetDayStatsOneShiftDept(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.one_shift_8_am_plant_settings)

    def test_get_dept_day_stats_first_shift(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_1_hours_per_unit_dict
        dept_list = ['DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8', 'DEPT9', 'OTHER']

        expected_hours_per_unit = 10
        expected_working_hours = 10

        for dept in dept_list:
            if dept == 'OTHER':
                expected_hours_per_unit = 0
                expected_working_hours = 0
            self.assertEqual(get_dept_day_stats(hours_per_unit_dict, now, dept),
                             (expected_hours_per_unit, expected_working_hours))


class GetDayhours_per_unitDict(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.two_shift_8_am_plant_settings)

    def test_get_day_hours_per_unit_dict(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
        settings = PlantSetting.objects.latest('timestamp')
        hours_per_unit_dict = tc.shift_2_hours_per_unit_dict_with_plant
        hours_per_unitATM.objects.create(**api_tc.two_shifts_first_shift_api_entry)

        expected_full_hours_per_unit_dict = tc.expected_full_hours_per_unit_dict

        self.assertEqual(get_day_hours_per_unit_dict(hours_per_unit_dict, now),
                         expected_full_hours_per_unit_dict)


class DeleteOldEntries(TestCase):
    def setUp(self):
        # Deletes after 1 day
        PlantSetting.objects.create(**ps_tc.default_plant_settings_with_del)
        # API 6/2 @ 7:00
        hours_per_unitATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_7_am)
        # API 6/2 @ 14:30
        hours_per_unitATM.objects.create(**api_tc.two_shifts_first_shift_api_entry)

    def test_delete_old_entries(self):
        now = timezone.make_aware(dt.datetime(2016, 6, 3, 12, 30))
        plant_settings = PlantSetting.objects.latest('timestamp')
        delete_old_entries(plant_settings, now)

        self.assertEqual(hours_per_unitATM.objects.count(), 1)


class NeedToWrite(TestCase):
    def setUp(self):
        PlantSetting.objects.create(**ps_tc.default_plant_settings_20_30)

        PlantActivityModel.objects.create(
            UNIT_NUM='HZ3852',
            UNIT_COMPLETED_DEPT='03',
            UNIT_LOADED_TIME=timezone.make_aware(dt.datetime(2016, 6, 2, 6, 55)),
        )

    def test_need_to_write_true_and_near_end(self):
        hours_per_unitATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_7_am)
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 14, 27))
        plant_settings = PlantSetting.objects.latest('timestamp')
        last_api_write = hours_per_unitATM.objects.filter(timestamp__lte=now)
        last_api_write = last_api_write.latest('timestamp')
        last_claim = PlantActivityModel.objects.filter(UNIT_COMPLETED_DEPT='03',
                                                     UNIT_LOADED_TIME__lte=now)
        last_claim = last_claim.latest('UNIT_LOADED_TIME')

        self.assertEqual(need_to_write(now, plant_settings, last_api_write, last_claim), True)

    def test_need_to_write_true_and_not_near_end(self):
        hours_per_unitATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_7_am)
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 12, 30))
        plant_settings = PlantSetting.objects.latest('timestamp')
        last_api_write = hours_per_unitATM.objects.filter(timestamp__lte=now)
        last_api_write = last_api_write.latest('timestamp')
        last_claim = PlantActivityModel.objects.filter(UNIT_COMPLETED_DEPT='03',
                                                     UNIT_LOADED_TIME__lte=now)
        last_claim = last_claim.latest('UNIT_LOADED_TIME')

        self.assertEqual(need_to_write(now, plant_settings, last_api_write, last_claim), True)

    def test_need_to_write_false_and_near_end(self):
        hours_per_unitATM.objects.create(**api_tc.two_shifts_first_shift_api_entry)
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 14, 27))
        plant_settings = PlantSetting.objects.latest('timestamp')
        last_api_write = hours_per_unitATM.objects.filter(timestamp__lte=now)
        last_api_write = last_api_write.latest('timestamp')
        last_claim = PlantActivityModel.objects.filter(UNIT_COMPLETED_DEPT='03',
                                                     UNIT_LOADED_TIME__lte=now)
        last_claim = last_claim.latest('UNIT_LOADED_TIME')

        self.assertEqual(need_to_write(now, plant_settings, last_api_write, last_claim), True)

    def test_need_to_write_false_and_not_near_end(self):
        hours_per_unitATM.objects.create(**api_tc.two_shifts_first_shift_api_entry_7_am)
        now = timezone.make_aware(dt.datetime(2016, 6, 2, 7, 5))
        plant_settings = PlantSetting.objects.latest('timestamp')
        last_api_write = hours_per_unitATM.objects.filter(timestamp__lte=now)
        last_api_write = last_api_write.latest('timestamp')
        last_claim = PlantActivityModel.objects.filter(UNIT_COMPLETED_DEPT='03',
                                                     UNIT_LOADED_TIME__lte=now)
        last_claim = last_claim.latest('UNIT_LOADED_TIME')

        self.assertEqual(need_to_write(now, plant_settings, last_api_write, last_claim), False)
