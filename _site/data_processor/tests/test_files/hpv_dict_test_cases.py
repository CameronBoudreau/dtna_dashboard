from django.utils import timezone
import datetime as dt


"""
hours_per_unit Dictionaries
"""
shift_1_hours_per_unit_dict = {'DEPT8': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'claims_for_range': 1, 'DEPT7': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT3': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT4': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'PLANT': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'shift': 1, 'DEPT2': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT1': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT6': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'OTHER': {'ne': 0, 'hours_per_unit': 0.0, 'mh': 0}, 'DEPT5': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT9': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}}

shift_1_hours_per_unit_dict_0_hours_per_unit = {'DEPT8': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'claims_for_range': 0, 'DEPT7': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT3': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT4': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'PLANT': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'shift': 1, 'DEPT2': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT1': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT6': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'OTHER': {'ne': 0, 'hours_per_unit': 0.0, 'mh': 0}, 'DEPT5': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT9': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}}

shift_1_hours_per_unit_dict_with_plant = {'DEPT8': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'claims_for_range': 1, 'DEPT7': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT3': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT4': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'PLANT': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'shift': 1, 'DEPT2': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT1': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT6': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'OTHER': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT5': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT9': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'plant_s_hours_per_unit': 90, 'plant_s_working_hours': 90, 'plant_s_ne': 90}

shift_1_hours_per_unit_dict_with_plant_0_hours_per_unit = {'DEPT8': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'claims_for_range': 0, 'DEPT7': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT3': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT4': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'PLANT': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'shift': 1, 'DEPT2': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT1': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT6': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'OTHER': {'ne': 0, 'hours_per_unit': 0.0, 'mh': 0}, 'DEPT5': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT9': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'plant_s_hours_per_unit': 0, 'plant_s_working_hours': 0, 'plant_s_ne': 0}

shift_2_hours_per_unit_dict = {'DEPT8': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'claims_for_range': 1, 'DEPT7': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT3': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT4': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'PLANT': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'shift': 2, 'DEPT2': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT1': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT6': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'OTHER': {'ne': 0, 'hours_per_unit': 0.0, 'mh': 0}, 'DEPT5': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT9': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}}

shift_2_hours_per_unit_dict_0_hours_per_unit = {'DEPT8': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'claims_for_range': 0, 'DEPT7': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT3': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT4': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'PLANT': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'shift': 2, 'DEPT2': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT1': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT6': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'OTHER': {'ne': 0, 'hours_per_unit': 0.0, 'mh': 0}, 'DEPT5': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT9': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}}

shift_2_hours_per_unit_dict_with_plant = {'DEPT8': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'claims_for_range': 1, 'DEPT7': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT3': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT4': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'PLANT': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'shift': 2, 'DEPT2': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT1': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT6': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'OTHER': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT5': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT9': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'plant_s_hours_per_unit': 90, 'plant_s_working_hours': 90,'plant_s_ne': 90,}

shift_2_hours_per_unit_dict_with_plant_0_hours_per_unit = {'DEPT8': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'claims_for_range': 0, 'DEPT7': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT3': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT4': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'PLANT': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'shift': 2, 'DEPT2': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT1': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT6': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'OTHER': {'ne': 0, 'hours_per_unit': 0.0, 'mh': 0}, 'DEPT5': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT9': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'plant_s_hours_per_unit': 0, 'plant_s_working_hours': 0, 'plant_s_ne': 0}

shift_3_hours_per_unit_dict = {'DEPT8': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'claims_for_range': 1, 'DEPT7': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT3': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT4': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'PLANT': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'shift': 3, 'DEPT2': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT1': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT6': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'OTHER': {'ne': 0, 'hours_per_unit': 0.0, 'mh': 0}, 'DEPT5': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT9': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}}

shift_3_hours_per_unit_dict_0_hours_per_unit = {'DEPT8': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'claims_for_range': 0, 'DEPT7': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT3': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT4': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'PLANT': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'shift': 3, 'DEPT2': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT1': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT6': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'OTHER': {'ne': 0, 'hours_per_unit': 0.0, 'mh': 0}, 'DEPT5': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT9': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}}

shift_3_hours_per_unit_dict_with_plant = {'DEPT8': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'claims_for_range': 1, 'DEPT7': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT3': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT4': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'PLANT': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'shift': 3, 'DEPT2': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT1': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT6': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'OTHER': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT5': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'DEPT9': {'ne': 10, 'hours_per_unit': 10, 'mh': 10}, 'plant_s_hours_per_unit': 90, 'plant_s_working_hours': 90, 'plant_s_ne': 90}

shift_3_hours_per_unit_dict_with_plant_0_hours_per_unit = {'DEPT8': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'claims_for_range': 0, 'DEPT7': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT3': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT4': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'PLANT': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'shift': 3, 'DEPT2': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT1': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT6': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'OTHER': {'ne': 0, 'hours_per_unit': 0.0, 'mh': 0}, 'DEPT5': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'DEPT9': {'ne': 0, 'hours_per_unit': 0, 'mh': 0}, 'plant_s_hours_per_unit': 0, 'plant_s_working_hours': 0, 'plant_s_ne': 0}


expected_full_hours_per_unit_dict = {
    'DEPT1_s_hours_per_unit': 10,
    'DEPT1_s_working_hours': 10,
    'DEPT1_s_ne': 10,
    'DEPT1_d_hours_per_unit': 10.0,
    'DEPT1_d_working_hours': 90.0,
    'DEPT2_s_hours_per_unit': 10.0,
    'DEPT2_s_working_hours': 10,
    'DEPT2_s_ne': 10,
    'DEPT2_d_hours_per_unit': 10.0,
    'DEPT2_d_working_hours': 90.0,
    'DEPT3_s_hours_per_unit': 10,
    'DEPT3_s_working_hours': 10,
    'DEPT3_s_ne': 10,
    'DEPT3_d_hours_per_unit': 10.0,
    'DEPT3_d_working_hours': 90.0,
    'DEPT4_s_hours_per_unit': 10,
    'DEPT4_s_working_hours': 10,
    'DEPT4_s_ne': 10,
    'DEPT4_d_hours_per_unit': 10.0,
    'DEPT4_d_working_hours': 90.0,
    'DEPT5_s_hours_per_unit': 10,
    'DEPT5_s_working_hours': 10,
    'DEPT5_s_ne': 10,
    'DEPT5_d_hours_per_unit': 10.0,
    'DEPT5_d_working_hours': 90.0,
    'DEPT6_s_hours_per_unit': 10,
    'DEPT6_s_working_hours': 10,
    'DEPT6_s_ne': 10,
    'DEPT6_d_hours_per_unit': 10.0,
    'DEPT6_d_working_hours': 90.0,
    'DEPT7_s_hours_per_unit': 10,
    'DEPT7_s_working_hours': 10,
    'DEPT7_s_ne': 10,
    'DEPT7_d_hours_per_unit': 10.0,
    'DEPT7_d_working_hours': 90.0,
    'DEPT8_s_hours_per_unit': 10,
    'DEPT8_s_working_hours': 10,
    'DEPT8_s_ne': 10,
    'DEPT8_d_hours_per_unit': 10.0,
    'DEPT8_d_working_hours': 90.0,
    'DEPT9_s_hours_per_unit': 10,
    'DEPT9_s_working_hours': 10,
    'DEPT9_s_ne': 10,
    'DEPT9_d_hours_per_unit': 10.0,
    'DEPT9_d_working_hours': 90.0,
    'OTHER_s_hours_per_unit': 0,
    'OTHER_s_working_hours': 0,
    'OTHER_s_ne': 0,
    'OTHER_d_hours_per_unit': 0,
    'OTHER_d_working_hours': 0,

    'PLANT_d_hours_per_unit': 90.0,
    'PLANT_d_working_hours': 810.0,
    'PLANT_s_hours_per_unit': 90.0,
    'PLANT_s_ne': 90.0,
    'PLANT_s_working_hours': 90.0,

    'claims_s': 1,
    'claims_d': 9,

    'shift': 2,
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 15, 30))
}
