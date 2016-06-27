from django.utils import timezone
import datetime as dt


@timezone.override("US/Eastern")
def get_shift_info(plant_settings, now):
    """
    Queries the plant settings to get the current shift and the time it started
    based on "now".

    :param now: The simulated time - datetime object.
    :param plant_settings: The most recent instance of the plant settings.
    :return: Integer value - shift number AND a datetime object - shift start
        time.
    """
    print("/"*50)
    print("GET SHIFT INFO")
    print("/"*50)
    print('plant_settings num of shifts: ', plant_settings.num_of_shifts)
    print('now: ', now)
    print("First_shift: ", plant_settings.first_shift)
    print("Second shift: ", plant_settings.second_shift)

    # SHIFT 1 SET UP
    shift = 1
    start = dt.datetime.combine(now.date(), plant_settings.first_shift)
    start = timezone.make_aware(start)
    print("MADE LOCAL timezone AWARE START")

    # OT SET UP
    first_ot = get_first_shift_ot(now, plant_settings)

    # Catch time before first shift if there are 3 shifts. Shift will have
    # started the day before.
    before_first_shift = now.time() < plant_settings.first_shift
    if before_first_shift and plant_settings.num_of_shifts == 3:
        print("SHIFTS=3")
        shift, start = get_third_shift_start(now, plant_settings)
    # Catch OT for 2nd shift from the previous day
    elif plant_settings.num_of_shifts == 2 and now.time() < first_ot:
        shift, start = get_second_shift_start(now, plant_settings)
    # Catch anything after first shift.
    elif now.time() >= plant_settings.first_shift:
        # If more than 1 shift, check which of those shifts we are in.
        shift, start = find_shift_after_first(now, plant_settings, shift,
                                              start)
    else:
        shift = 1
        start = dt.datetime.combine(now.date(), dt.time(0, 0))
        start = timezone.make_aware(start)

    print('START: ', start)
    print('SHIFT: ', shift)

    return start, shift


def get_first_shift_ot(now, plant_settings):
    """
    Finds the start time of overtime for first shift.

    :param now: The simulated time - datetime object.
    :param plant_settings: The most recent instance of the plant settings.
    :return: Datetime object - when overtime starts for first shift.
    """
    # Have to convert to datetime subtract timedelta, then back to time object
    first_shift_date = dt.datetime.combine(now.date(),
                                           plant_settings.first_shift)
    first_ot = first_shift_date - dt.timedelta(hours=3, minutes=30)
    first_ot = first_ot.time()
    return first_ot


def find_shift_after_first(now, plant_settings, shift, start):
    """
    Called when the time is past the first shift and checks if it is late
    enough to be in any following shifts should they exist.

    :param now: The simulated time - datetime object.
    :param plant_settings: The most recent instance of the plant settings.
    :param shift: Integer - current shift.
    :param start: Datetime object - current shift start time.
    :return: Integer - shift AND a datetime object - start.
    """
    # If 2 shifts and past the start of the second
    if plant_settings.num_of_shifts >= 2:
        print("2 or MORE SHIFTS ACTIVATED")
        if now.time() >= plant_settings.second_shift:
            print("2nd 3 SHIFT CHECK")
            shift = 2
            start = dt.datetime.combine(now.date(),
                                        plant_settings.second_shift)
            start = timezone.make_aware(start)
            # If 3 shifts, check if time is in that shift.
            print("2nd 3 SHIFT CHECK")
            if plant_settings.num_of_shifts == 3:
                shift, start = check_if_in_third_shift(now, plant_settings,
                                                       shift, start)

    return shift, start


def check_if_in_third_shift(now, plant_settings, shift, start):
    """
    Called when the time is past the first shift. Sets the shift and start
    times for third shift if time is past third shift start times. Date is set
    to today as opposed to the previous day in this case

    :param now: The simulated time - datetime object.
    :param plant_settings: The most recent instance of the plant settings.
    :param shift: Integer - current shift.
    :param start: Datetime object - current shift start time.
    :return: Integer - shift AND a datetime object - start.
    """
    if now.time() >= plant_settings.third_shift:
        shift = 3
        start = dt.datetime.combine(now.date(), plant_settings.third_shift)
        start = timezone.make_aware(start)
    return shift, start


def get_third_shift_start(now, plant_settings):
    """
    Called when 3 shifts are found and the time is before the start of shift
    one. Sets the start of shift 3 back one day.

    :param now: The simulated time - datetime object.
    :param plant_settings: The most recent instance of the plant settings.
    :return: Integer value - shift AND a datetime object - when third shift
        starts.
    """
    shift = 3
    yesterday = (now.date() - dt.timedelta(days=1))
    start = dt.datetime.combine(yesterday, plant_settings.third_shift)
    start = timezone.make_aware(start)
    print("START TIME FOR 3 SHIFTS = ", start)

    return shift, start


def get_second_shift_start(now, plant_settings):
    """
    Called when "now" is in shift 2 and sets the shift and shift start times.

    :param now: The simulated time - datetime object.
    :param plant_settings: The most recent instance of the plant settings.
    :return: Integer value - shift AND a datetime object - when second shift
        starts.
    """
    shift = 2
    yesterday = (now.date() - dt.timedelta(days=1))
    start = dt.datetime.combine(yesterday, plant_settings.second_shift)
    start = timezone.make_aware(start)

    return shift, start


def get_day_start(plant_settings, now):
    """
    Finds the start of the day based on number of shifts set in plant settings
    and the current time

    :param plant_settings: The most recent instance of the plant settings.
    :param now: The simulated time - datetime object.
    :return: Datetime object - day start time and date (could be the previous
        day)
    """
    # Find if now is in the second shift's overtime period
    in_second_ot = dt.time(0, 0) < now.time() < get_first_shift_ot(
        now, plant_settings
    )
    # Find the date yesterday
    yesterday = (now - dt.timedelta(days=1)).date()
    # If 3 shifts and now is before the start of the third shift, start is the
    # day before. Else same day at shift start.
    if plant_settings.num_of_shifts == 3:
        if now.time() >= plant_settings.third_shift:
            day_start = dt.datetime.combine(now.date(),
                                            plant_settings.third_shift)
        else:
            day_start = dt.datetime.combine(yesterday,
                                            plant_settings.third_shift)
    # If two shifts and data was found before the start of first shift's OT,
    # the day starts yesterday at first shift
    elif plant_settings.num_of_shifts == 2:
        if in_second_ot:
            day_start = dt.datetime.combine(yesterday,
                                            plant_settings.first_shift)
        else:
            day_start = dt.datetime.combine(now.date(),
                                            plant_settings.first_shift)
    else:
        day_start = dt.datetime.combine(now.date(), plant_settings.first_shift)
    return timezone.localtime(timezone.make_aware(day_start))
