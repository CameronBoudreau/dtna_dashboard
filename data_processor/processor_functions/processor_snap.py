from data_processor.functions.process_data_main import main
from .processor_shift import get_shift_info
from plantsettings.models import PlantSetting


def get_hours_per_unit_snap(now):
    """
    Finds the current shift and its start time to pass on to the functions that
    calculate hours_per_unit by department and shift.

    :param now: The simulated time - datetime object.
    :return: Dictionary of department keys each containing a dictionary of
        manhours, number clocked in, and hours_per_unit for the current shift.
    """
    print("/"*50)
    print("GET hours_per_unit SNAP")
    print("/"*50)
    plant_settings = PlantSetting.objects.latest('timestamp')
    # print("SETINGS",settings.timestamp)
    print("NOW: ", now)
    # preventing processing data before start of defined shift
    start, shift = get_shift_info(plant_settings, now)
    print("Start: ", start)
    print("Shift: ", shift)

    if start > now:
        print("NOT IN SHIFT")
        return
    hours_per_unit_dict = main(start, now)
    hours_per_unit_dict['shift'] = shift

    return hours_per_unit_dict
