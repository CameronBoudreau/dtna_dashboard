from django.utils import timezone
import datetime as dt


"""
Plant Settings
"""
default_plant_settings_20_30 = {
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 7, 0)),
    'plant_code': '017',
    'plant_target': 55,
    'num_of_shifts': 2,
    'first_shift': dt.time(6,30),
    'second_shift': dt.time(14,30),
    'third_shift': dt.time(22,30),
    'dripper_start': timezone.make_aware(dt.datetime(2016, 6, 2, 20, 30))
}

default_plant_settings_with_del = {
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 7, 0)),
    'plant_code': '017',
    'plant_target': 55,
    'num_of_shifts': 2,
    'del_after': 1,
    'first_shift': dt.time(6,30),
    'second_shift': dt.time(14,30),
    'third_shift': dt.time(22,30),
    'dripper_start': timezone.make_aware(dt.datetime(2016, 6, 2, 20, 30))
}


default_plant_settings_near_shift_end = {
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 0, 0)),
    'plant_code': '017',
    'plant_target': 55,
    'num_of_shifts': 2,
    'first_shift': dt.time(6,30),
    'second_shift': dt.time(14,30),
    'third_shift': dt.time(22,30),
    'dripper_start': timezone.make_aware(dt.datetime(2016, 6, 2, 14, 27))
}

default_plant_settings_7_05 = {
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 0, 0)),
    'plant_code': '017',
    'plant_target': 55,
    'num_of_shifts': 2,
    'first_shift': dt.time(6,30),
    'second_shift': dt.time(14,30),
    'third_shift': dt.time(22,30),
    'dripper_start': timezone.make_aware(dt.datetime(2016, 6, 2, 7, 5))
}

default_plant_settings_14_27 = {
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 0, 0)),
    'plant_code': '017',
    'plant_target': 55,
    'num_of_shifts': 2,
    'first_shift': dt.time(6,30),
    'second_shift': dt.time(14,30),
    'third_shift': dt.time(22,30),
    'dripper_start': timezone.make_aware(dt.datetime(2016, 6, 2, 14, 27))
}

default_plant_settings_18_00_6_3 = {
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 0, 0)),
    'plant_code': '017',
    'plant_target': 55,
    'num_of_shifts': 2,
    'first_shift': dt.time(6,30),
    'second_shift': dt.time(14,30),
    'third_shift': dt.time(22,30),
    'dripper_start': timezone.make_aware(dt.datetime(2016, 6, 3, 18, 0))
}

three_shift_8_am_plant_settings = {
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 7, 0)),
    'plant_code': '017',
    'plant_target': 55,
    'num_of_shifts': 3,
    'first_shift': dt.time(6,30),
    'second_shift': dt.time(14,30),
    'third_shift': dt.time(22,30),
    'dripper_start': timezone.make_aware(dt.datetime(2016, 6, 2, 8, 0))
}

two_shift_8_am_plant_settings = {
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 7, 0)),
    'plant_code': '017',
    'plant_target': 55,
    'num_of_shifts': 2,
    'first_shift': dt.time(6,30),
    'second_shift': dt.time(14,30),
    'third_shift': dt.time(22,30),
    'dripper_start': timezone.make_aware(dt.datetime(2016, 6, 2, 8, 0))
}

one_shift_8_am_plant_settings = {
    'timestamp': timezone.make_aware(dt.datetime(2016, 6, 2, 7, 0)),
    'plant_code': '017',
    'plant_target': 55,
    'num_of_shifts': 1,
    'first_shift': dt.time(6,30),
    'second_shift': dt.time(14,30),
    'third_shift': dt.time(22,30),
    'dripper_start': timezone.make_aware(dt.datetime(2016, 6, 2, 8, 0))
}
