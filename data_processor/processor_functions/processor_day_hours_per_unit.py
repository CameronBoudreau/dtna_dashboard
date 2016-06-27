from .processor_plant_stats import get_plant_stats, calc_plant_hours_per_unit_for_shift
from .processor_dept_day_stats import get_dept_day_stats
from .processor_plant_day_stats import get_plant_day_hours_per_unit

from django.utils import timezone


def get_day_hours_per_unit_dict(hours_per_unit_dict, now):
    """
    Calculates the day total hours_per_unit and manhours based on current values since
    shift start and adding these to the last recorded value of the any previous
    shifts if applicable.

    :param hours_per_unit_dict: A dictionary object containing hours_per_unit, manhours, number
        clocked in by department as well as number of claims that shift.
    :param now: The simulated time - datetime object.
    :return: Dictionary object to be written to the api.
    """
    print("/"*50)
    print("GET DAY hours_per_unit DICT FUNCTION")
    print("/"*50)

    # Department list to loop through
    dept_list = [
        'DEPT1', 'DEPT2', 'DEPT3', 'DEPT4', 'DEPT5', 'DEPT6', 'DEPT7', 'DEPT8', 'DEPT9', 'OTHER'
        ]
    dept_values = []
    full_dict = {}

    # Adds dept shift values for manhours and number in to get plant shift info
    plant_s_working_hours, plant_s_ne = get_plant_stats(hours_per_unit_dict, dept_list)
    # hours_per_unit calculated based on manhours/claims
    plant_s_hours_per_unit = calc_plant_hours_per_unit_for_shift(hours_per_unit_dict, plant_s_working_hours)

    # Calculates the stats for the day by department.
    for dept in dept_list:
        dept_values.append(get_dept_day_stats(hours_per_unit_dict, now, dept))

    print("DEPT_VALUES ", dept_values)

    # Dictionary to update 2 others with plant data.
    shift_dict = {
        'plant_s_hours_per_unit': plant_s_hours_per_unit,
        'plant_s_working_hours': plant_s_working_hours,
        'plant_s_ne': plant_s_ne,
    }

    # hours_per_unit dict updated to calc plant day totals further on.
    hours_per_unit_dict.update(shift_dict)
    # Adds to dictionary that will be returned
    full_dict.update(shift_dict)
    print('FULL DICT:', full_dict)

    # Calculates the day totals for the plant
    plant_d_hours_per_unit, plant_d_working_hours, claims_d = get_plant_day_hours_per_unit(hours_per_unit_dict, now)
    print("plant_d_hours_per_unit, plant_d_working_hours, claims_d= ",
          plant_d_hours_per_unit, plant_d_working_hours, claims_d)

    # Fills the dictionary that will be written to API
    full_hours_per_unit_dict = {
        'DEPT1_s_hours_per_unit': hours_per_unit_dict['DEPT1']['hours_per_unit'],
        'DEPT1_s_working_hours': hours_per_unit_dict['DEPT1']['mh'],
        'DEPT1_s_ne': hours_per_unit_dict['DEPT1']['ne'],
        'DEPT1_d_hours_per_unit': dept_values[0][0],
        'DEPT1_d_working_hours': dept_values[0][1],
        'DEPT2_s_hours_per_unit': hours_per_unit_dict['DEPT2']['hours_per_unit'],
        'DEPT2_s_working_hours': hours_per_unit_dict['DEPT2']['mh'],
        'DEPT2_s_ne': hours_per_unit_dict['DEPT2']['ne'],
        'DEPT2_d_hours_per_unit': dept_values[1][0],
        'DEPT2_d_working_hours': dept_values[1][1],
        'DEPT3_s_hours_per_unit': hours_per_unit_dict['DEPT3']['hours_per_unit'],
        'DEPT3_s_working_hours': hours_per_unit_dict['DEPT3']['mh'],
        'DEPT3_s_ne': hours_per_unit_dict['DEPT3']['ne'],
        'DEPT3_d_hours_per_unit': dept_values[2][0],
        'DEPT3_d_working_hours': dept_values[2][1],
        'DEPT4_s_hours_per_unit': hours_per_unit_dict['DEPT4']['hours_per_unit'],
        'DEPT4_s_working_hours': hours_per_unit_dict['DEPT4']['mh'],
        'DEPT4_s_ne': hours_per_unit_dict['DEPT4']['ne'],
        'DEPT4_d_hours_per_unit': dept_values[3][0],
        'DEPT4_d_working_hours': dept_values[3][1],
        'DEPT5_s_hours_per_unit': hours_per_unit_dict['DEPT5']['hours_per_unit'],
        'DEPT5_s_working_hours': hours_per_unit_dict['DEPT5']['mh'],
        'DEPT5_s_ne': hours_per_unit_dict['DEPT5']['ne'],
        'DEPT5_d_hours_per_unit': dept_values[4][0],
        'DEPT5_d_working_hours': dept_values[4][1],
        'DEPT6_s_hours_per_unit': hours_per_unit_dict['DEPT6']['hours_per_unit'],
        'DEPT6_s_working_hours': hours_per_unit_dict['DEPT6']['mh'],
        'DEPT6_s_ne': hours_per_unit_dict['DEPT6']['ne'],
        'DEPT6_d_hours_per_unit': dept_values[5][0],
        'DEPT6_d_working_hours': dept_values[5][1],
        'DEPT7_s_hours_per_unit': hours_per_unit_dict['DEPT7']['hours_per_unit'],
        'DEPT7_s_working_hours': hours_per_unit_dict['DEPT7']['mh'],
        'DEPT7_s_ne': hours_per_unit_dict['DEPT7']['ne'],
        'DEPT7_d_hours_per_unit': dept_values[6][0],
        'DEPT7_d_working_hours': dept_values[6][1],
        'DEPT8_s_hours_per_unit': hours_per_unit_dict['DEPT8']['hours_per_unit'],
        'DEPT8_s_working_hours': hours_per_unit_dict['DEPT8']['mh'],
        'DEPT8_s_ne': hours_per_unit_dict['DEPT8']['ne'],
        'DEPT8_d_hours_per_unit': dept_values[7][0],
        'DEPT8_d_working_hours': dept_values[7][1],
        'DEPT9_s_hours_per_unit': hours_per_unit_dict['DEPT9']['hours_per_unit'],
        'DEPT9_s_working_hours': hours_per_unit_dict['DEPT9']['mh'],
        'DEPT9_s_ne': hours_per_unit_dict['DEPT9']['ne'],
        'DEPT9_d_hours_per_unit': dept_values[8][0],
        'DEPT9_d_working_hours': dept_values[8][1],
        'OTHER_s_hours_per_unit': hours_per_unit_dict['OTHER']['hours_per_unit'],
        'OTHER_s_working_hours': hours_per_unit_dict['OTHER']['mh'],
        'OTHER_s_ne': hours_per_unit_dict['OTHER']['ne'],
        'OTHER_d_hours_per_unit': dept_values[9][0],
        'OTHER_d_working_hours': dept_values[9][1],

        'PLANT_d_hours_per_unit': plant_d_hours_per_unit,
        'PLANT_d_working_hours': plant_d_working_hours,
        'PLANT_s_hours_per_unit': plant_s_hours_per_unit,
        'PLANT_s_ne': plant_s_ne,
        'PLANT_s_working_hours': plant_s_working_hours,

        'claims_s': hours_per_unit_dict['claims_for_range'],
        'claims_d': claims_d,

        'shift': hours_per_unit_dict['shift'],
        'timestamp': timezone.localtime(now),
    }

    print("FULL DICT ", full_hours_per_unit_dict)
    return full_hours_per_unit_dict
