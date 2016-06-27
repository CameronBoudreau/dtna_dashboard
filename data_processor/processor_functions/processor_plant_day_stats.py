from plantsettings.models import PlantSetting
from api.models import hours_per_unitATM
from .processor_shift import get_day_start
from .processor_hours_per_unit_calc import calc_hours_per_unit


def get_plant_day_hours_per_unit(hours_per_unit_dict, now):
    """
    Calculates the hours_per_unit for the day by dividing shift manhours by the claims. If
    no claims, hours_per_unit is set to 0 to avoid a DivisionByZero error.

    :param hours_per_unit_dict: A dictionary object containing hours_per_unit, manhours, number
        clocked in by plant as well as number of claims that shift.
    :param now: The simulated time - datetime object.
    :return: Float value - plant day hours_per_unit AND Integer - manhours AND Integer -
        claims.
    """
    print("/"*50)
    print("GET DAY STATS FUNCTION")
    print("/"*50)
    print("NOW ", now)

    # Find latest plant settings and the start of the day based on number of
    # shifts in settings and current time
    plant_settings = PlantSetting.objects.latest('timestamp')
    day_start = get_day_start(plant_settings, now)

    # Gets all api entries for the day.
    all_since_start = hours_per_unitATM.objects.filter(timestamp__gte=day_start)

    # Set the current shift values to the hours_per_unit_dict values
    cur_hours_per_unit = hours_per_unit_dict['plant_s_hours_per_unit']
    cur_working_hours = hours_per_unit_dict['plant_s_working_hours']
    cur_claims = hours_per_unit_dict['claims_for_range']

    # Calc hours_per_unit based on time and number of shifts
    if plant_settings.num_of_shifts == 3:
        hours_per_unit, mh, claims = get_three_shifts_plant_day_hours_per_unit(
            hours_per_unit_dict, all_since_start, cur_hours_per_unit, cur_working_hours, cur_claims
        )
    elif plant_settings.num_of_shifts == 2:
        hours_per_unit, mh, claims = get_two_shifts_plant_day_hours_per_unit(
            hours_per_unit_dict, all_since_start, cur_hours_per_unit, cur_working_hours, cur_claims
        )
    else:
        hours_per_unit, mh, claims = cur_hours_per_unit, cur_working_hours, cur_claims
    return hours_per_unit, mh, claims


def get_three_shifts_plant_day_hours_per_unit(hours_per_unit_dict, all_since_start, cur_hours_per_unit, cur_working_hours,
                                   cur_claims):
    """
    Calculates the hours_per_unit for the plant based on 3 shifts active in settings. Gets
    the final snapshots from previous shifts to add to the current shift
    values. hours_per_unit is calculated based on manhour and claim totals for the day so
    far.

    :param hours_per_unit_dict: A dictionary object containing hours_per_unit, manhours, number
        clocked in by plant as well as number of claims that shift.
    :param all_since_start: Queryset object - API entries since the start of
        the day
    :param cur_hours_per_unit: shift hours_per_unit value for the plant - float.
    :param cur_working_hours: shift manhours value for the plant - integer.
    :param cur_claims: shift claims value - integer.
    :return: Float value - plant day hours_per_unit AND Integer - manhours AND Integer
        claims.
    """
    if hours_per_unit_dict['shift'] == 3:
        return cur_hours_per_unit, cur_working_hours, cur_claims
    # If in a later shift, add previous shift info
    elif hours_per_unit_dict['shift'] == 1:
        last_shift = all_since_start.filter(shift=3).last()
        hours_per_unit, mh, claims = get_last_shift_plant_day_hours_per_unit(cur_hours_per_unit, cur_working_hours,
                                                       cur_claims, last_shift)
    elif hours_per_unit_dict['shift'] == 2:
        s3 = all_since_start.filter(shift=3).last()
        s1 = all_since_start.filter(shift=1).last()
        hours_per_unit, mh, claims = get_three_shifts_plant_day_hours_per_unit_2nd_shift(s3, s1,
                                                                   cur_working_hours,
                                                                   cur_claims)
    return hours_per_unit, mh, claims


def get_three_shifts_plant_day_hours_per_unit_2nd_shift(s3, s1, cur_working_hours, cur_claims):
    """
    Calculates the hours_per_unit for the plant based on 3 shifts active in settings and
    "now" being in the second shift. Gets the final snapshots from previous
    shifts to add to the current shift values. hours_per_unit is calculated based on
    manhour and claim totals for the day so far.

    :param s3: hours_per_unitATM model instance - final entry for today's third shift.
    :param s1: hours_per_unitATM model instance - final entry for today's first shift.
        clocked in by plant as well as number of claims that shift.
    :param cur_working_hours: shift manhours value for the plant - integer.
    :param cur_claims: shift claims value - integer.
    :return: Float value - plant day hours_per_unit AND Integer - manhours AND Integer -
        claims.
    """
    # Check for missing api entries and calc with existing data
    if s3 is None:
        if s1 is None:
            mh = cur_working_hours
            claims = cur_claims
        else:
            mh = s1.PLANT_s_working_hours + cur_working_hours
            claims = s1.claims_s + cur_claims
    # Already checked for s3 is None, so we know it exists at this point
    elif s1 is None:
        mh = s3.PLANT_s_working_hours + cur_working_hours
        claims = s3.claims_s + cur_claims
    else:
        mh = s3.PLANT_s_working_hours + s1.PLANT_s_working_hours + cur_working_hours
        claims = s3.claims_s + s1.claims_s + cur_claims
    hours_per_unit = calc_hours_per_unit(mh, claims)

    return hours_per_unit, mh, claims


def get_two_shifts_plant_day_hours_per_unit(hours_per_unit_dict, all_since_start, cur_hours_per_unit, cur_working_hours,
                                 cur_claims):
    """
    Calculates the hours_per_unit for the plant based on 2 shifts active in settings. Gets
    the final snapshots from the previous shift to add to the current shift
    values. hours_per_unit is calculated based on manhour and claim totals for the day so
    far.

    :param hours_per_unit_dict: A dictionary object containing hours_per_unit, manhours, number
        clocked in by plant as well as number of claims that shift.
    :param all_since_start: Queryset object - API entries since the start of
        the day
    :param cur_hours_per_unit: shift hours_per_unit value for the plant - float.
    :param cur_working_hours: shift manhours value for the plant - integer.
    :param cur_claims: shift claims value - integer.
    :return: Float value - plant day hours_per_unit AND Integer - manhours AND Integer -
    claims.
    """
    if hours_per_unit_dict['shift'] == 1:
        hours_per_unit, mh, claims = cur_hours_per_unit, cur_working_hours, cur_claims
    elif hours_per_unit_dict['shift'] == 2:
        last_shift = all_since_start.filter(shift=1).last()
        hours_per_unit, mh, claims = get_last_shift_plant_day_hours_per_unit(cur_hours_per_unit, cur_working_hours,
                                                       cur_claims, last_shift)
    return hours_per_unit, mh, claims


def get_last_shift_plant_day_hours_per_unit(cur_hours_per_unit, cur_working_hours, cur_claims, last_shift):
    """
    Calculates the hours_per_unit for the plant based on only 1 previous shift. Gets the
    final snapshots from the previous shift to add to the current shift values.
    hours_per_unit is calculated based on manhour and claim totals for the day so far.

    :param cur_hours_per_unit: shift hours_per_unit value for the plant - float.
    :param cur_working_hours: shift manhours value for the plant - integer.
    :param cur_claims: shift claims value - integer.
    :param last_shift: hours_per_unitATM model object - API entry for the previous shift.
    :return: Float value - plant day hours_per_unit AND Integer - manhours.
    """
    if last_shift is None or last_shift.PLANT_s_working_hours is None:
        hours_per_unit = cur_hours_per_unit
        mh = cur_working_hours
        claims = cur_claims
    else:
        mh = float(last_shift.PLANT_s_working_hours) + cur_working_hours
        claims = last_shift.claims_s + cur_claims
        hours_per_unit = calc_hours_per_unit(mh, claims)
    return hours_per_unit, mh, claims
