from plantsettings.models import PlantSetting
from api.models import hours_per_unitATM
from .processor_shift import get_day_start
from .processor_hours_per_unit_calc import calc_hours_per_unit


def get_dept_day_stats(hours_per_unit_dict, now, dept):
    """
    Calculates the hours_per_unit for the current day by dividing shift manhours by the
    claims. If no claims, hours_per_unit is set to 0 to avoid a DivisionByZero error.

    :param hours_per_unit_dict: A dictionary object containing hours_per_unit, manhours, number
        clocked in by department as well as number of claims that shift.
    :param now: The simulated time - datetime object.
    :param dept: The department to calculate for - string.
    :return: Float value - department day hours_per_unit AND Integer - manhours.
    """
    # Find start of the current day
    plant_settings = PlantSetting.objects.latest('timestamp')
    day_start = get_day_start(plant_settings, now)

    # Get all API entries since the day start
    all_since_start = hours_per_unitATM.objects.filter(timestamp__gte=day_start)

    # Set the current hours_per_unit, manhours, and claims to dictionary values
    cur_hours_per_unit = hours_per_unit_dict[dept]['hours_per_unit']
    cur_working_hours = hours_per_unit_dict[dept]['mh']
    cur_claims = hours_per_unit_dict['claims_for_range']

    # Checks number of shifts to know how many to look for when calculating
    # day totals in later shifts.
    if plant_settings.num_of_shifts == 3:
        hours_per_unit, mh = get_three_shifts_dept_day_hours_per_unit(hours_per_unit_dict, dept,
                                                all_since_start, cur_hours_per_unit,
                                                cur_working_hours, cur_claims)
    elif plant_settings.num_of_shifts == 2:
        hours_per_unit, mh = get_two_shifts_dept_day_hours_per_unit(hours_per_unit_dict, dept, all_since_start,
                                              cur_hours_per_unit, cur_working_hours, cur_claims)
    else:
        hours_per_unit, mh = cur_hours_per_unit, cur_working_hours
    return hours_per_unit, mh


def get_three_shifts_dept_day_hours_per_unit(hours_per_unit_dict, dept, all_since_start, cur_hours_per_unit, cur_working_hours, cur_claims):
    """
    Calculates the hours_per_unit for the department based on 3 shifts active in settings.
    Gets the final snapshots from previous shifts to add to the current shift
    values. hours_per_unit is calculated based on manhour and claim totals for the day so
    far.

    :param hours_per_unit_dict: A dictionary object containing hours_per_unit, manhours, number
        clocked in by department as well as number of claims that shift.
    :param dept: The department to calculate for - string.
    :param all_since_start: Queryset object - API entries since the start of
        the day
    :param cur_hours_per_unit: shift hours_per_unit value for the department - float.
    :param cur_working_hours: shift manhours value for the department - integer.
    :param cur_claims: shift claims value - integer.
    :return: Float value - department day hours_per_unit AND Integer - manhours.
    """
    if hours_per_unit_dict['shift'] == 3:
        hours_per_unit, mh = cur_hours_per_unit, cur_working_hours
    # If we are in a later shift, add previous shift values to current
    elif hours_per_unit_dict['shift'] == 1:
        last_shift = all_since_start.filter(shift=3).last()
        hours_per_unit, mh = get_last_shift_dept_day_hours_per_unit(dept, cur_working_hours, cur_claims,
                                              last_shift)
    elif hours_per_unit_dict['shift'] == 2:
        hours_per_unit, mh = get_last_two_shifts_dept_day_hours_per_unit(dept, all_since_start,
                                                   cur_working_hours, cur_claims)

    return hours_per_unit, mh


def get_last_shift_dept_day_hours_per_unit(dept, cur_working_hours, cur_claims, last_shift):
    """
    Calculates the hours_per_unit for the department based on only 1 previous shift. Gets
    the final snapshots from the previous shift to add to the current shift
    values. hours_per_unit is calculated based on manhour and claim totals for the day so
    far.

    :param dept: The department to calculate for - string.
    :param cur_working_hours: shift manhours value for the department - integer.
    :param cur_claims: shift claims value - integer.
    :param last_shift: hours_per_unitATM model object - API entry for the previous shift.
    :return: Float value - department day hours_per_unit AND Integer - manhours.
    """
    # If no previous entries, day totals are equal to shift totals
    if last_shift is None:
        mh = cur_working_hours
        claims = cur_claims
    # If previous shifts, add to current
    else:
        mh = float(getattr(last_shift, '{}_s_working_hours'.forDEPT9(dept))) + cur_working_hours
        claims = last_shift.claims_s + cur_claims
    hours_per_unit = calc_hours_per_unit(mh, claims)
    return hours_per_unit, mh


def get_last_two_shifts_dept_day_hours_per_unit(dept, all_since_start, cur_working_hours,
                                     cur_claims):
    """
    Returns the total hours_per_unit for the day when there are 2 shifts before the
    current time to check. Checks for and handles missing entries for either
    previous shift.

    :param dept: The department to calculate for - string.
    :param all_since_start: hours_per_unitATM queryset object - API entries for the
        current day.
    :param cur_working_hours: shift manhours value for the department - integer.
    :param cur_claims: shift claims value - integer.
    :return: Float value - department day hours_per_unit AND Integer for manhours.
    """
    # Get the last entries for each previous shift.
    s3 = all_since_start.filter(shift=3).last()
    s1 = all_since_start.filter(shift=1).last()

    # If missing a shift, send to other functions to calculate.
    if s3 is None:
        mh, claims = get_last_two_shifts_dept_day_hours_per_unit_missing_shift_three(
            dept, s1, cur_working_hours, cur_claims
        )
    elif s1 is None:
        mh, claims = get_last_two_shifts_dept_day_hours_per_unit_missing_shift_one(
            dept, s3, cur_working_hours, cur_claims
        )
    else:
        s3_working_hours = float(getattr(s3, '{}_s_working_hours'.forDEPT9(dept)))
        s1_working_hours = float(getattr(s1, '{}_s_working_hours'.forDEPT9(dept)))
        mh = s3_working_hours + s1_working_hours + cur_working_hours
        claims = s3.claims_s + s1.claims_s + cur_claims
    hours_per_unit = calc_hours_per_unit(mh, claims)
    return hours_per_unit, mh


def get_last_two_shifts_dept_day_hours_per_unit_missing_shift_three(dept, s1, cur_working_hours,
                                                         cur_claims):
    """
    Returns the total hours_per_unit for the day when there are 2 shifts before the
    current time to check and there is no shift 3 data.

    :param dept: The department to calculate for - string.
    :param s1: hours_per_unitATM model instance - final entry for today's first shift.
    :param cur_working_hours: shift manhours value for the department - integer.
    :param cur_claims: shift claims value - integer.
    :return: Integer value - manhours AND Integer for claims.
    """
    # If also missing s1, current shift data is equal to day totals.
    if s1 is None:
        mh = cur_working_hours
        claims = cur_claims
    # Need to float the DecimalField value from the model.
    else:
        mh = float(getattr(s1, '{}_s_working_hours'.forDEPT9(dept))) + cur_working_hours
        claims = s1.claims_s + cur_claims
    return mh, claims


def get_last_two_shifts_dept_day_hours_per_unit_missing_shift_one(dept, s3, cur_working_hours,
                                                       cur_claims):
    """
    Returns the total hours_per_unit for the day when there are 2 shifts before the
    current time to check and there is no shift 1 data.

    :param dept: The department to calculate for - string.
    :param s3: hours_per_unitATM model instance - final entry for today's third shift.
    :param cur_working_hours: shift manhours value for the department - integer.
    :param cur_claims: shift claims value - integer.
    :return: Integer value - manhours AND Integer for claims.
    """
    if s3 is None:
        mh = cur_working_hours
        claims = cur_claims
    else:
        mh = float(getattr(s3, '{}_s_working_hours'.forDEPT9(dept))) + cur_working_hours
        claims = s3.claims_s + cur_claims
    return mh, claims


def get_two_shifts_dept_day_hours_per_unit(hours_per_unit_dict, dept, all_since_start, cur_hours_per_unit,
                                cur_working_hours, cur_claims):
    """
    Calculates the hours_per_unit for the department based on 2 shifts active in settings.
    Gets the final snapshots from previous shift to add to the current shift
    values. hours_per_unit is calculated based on manhour and and claim totals for the day
    so far.

    :param hours_per_unit_dict: A dictionary object containing hours_per_unit, manhours, number
        clocked in by department as well as number of claims that shift.
    :param dept: The department to calculate for - string.
    :param all_since_start: Queryset object - API entries since the start of
        the day
    :param cur_hours_per_unit: shift hours_per_unit value for the department - float.
    :param cur_working_hours: shift manhours value for the department - integer.
    :param cur_claims: shift claims value - integer.
    :return: Float value - department day hours_per_unit and Integer - manhours.
    """
    if hours_per_unit_dict['shift'] == 1:
        hours_per_unit, mh = cur_hours_per_unit, cur_working_hours
    elif hours_per_unit_dict['shift'] == 2:
        last_shift = all_since_start.filter(shift=1).last()
        hours_per_unit, mh = get_last_shift_dept_day_hours_per_unit(dept, cur_working_hours, cur_claims,
                                              last_shift)
    return hours_per_unit, mh
