def get_plant_stats(hours_per_unit_dict, dept_list):
    """
    Loops through department info in hours_per_unit_dict to get plant totals.

    :param hours_per_unit_dict: A dictionary object containing hours_per_unit, manhours, number
        clocked in by department and total for the plant as well as number of
        claims that shift.
    :param dept_list: Array of strings - department labels.
    :return: Integer values - plant manhours AND plant total clocked in
        employees.
    """
    plant_s_ne = 0
    plant_s_working_hours = 0
    for dept in dept_list:
        plant_s_working_hours += hours_per_unit_dict[dept]['mh']
        plant_s_ne += hours_per_unit_dict[dept]['ne']
    return plant_s_working_hours, plant_s_ne


def calc_plant_hours_per_unit_for_shift(hours_per_unit_dict, plant_s_working_hours):
    """
    Calculates the hours_per_unit for the current shift by dividing shift manhours by the
    claims. If no claims, hours_per_unit is set to 0 to avoid a DivisionByZero error.

    :param hours_per_unit_dict: A dictionary object containing hours_per_unit, manhours, number
        clocked in by department and total for the plant as well as number of
        claims that shift.
    :param plant_s_working_hours: Integer value - plant manhours for the shift.
    :return: Float value - plant shift hours_per_unit.
    """
    if hours_per_unit_dict['claims_for_range'] == 0 or hours_per_unit_dict is None:
        plant_s_hours_per_unit = 0
    else:
        plant_s_hours_per_unit = plant_s_working_hours / hours_per_unit_dict['claims_for_range']
    return plant_s_hours_per_unit
