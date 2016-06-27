from api.models import hours_per_unitATM
from plantsettings.models import PlantSetting
from .processor_time import get_time_with_timezone
from .processor_table_entries import get_last_api_write, get_last_claim
from .processor_write_conditions import need_to_write, no_dict_or_no_claims
from .processor_snap import get_hours_per_unit_snap
from .processor_day_hours_per_unit import get_day_hours_per_unit_dict
from .processor_delete_old import delete_old_entries


def get_new_hours_per_unit_data():
    """
    Checks the server for new claim data. Checks that claims exist and that
    there is a new claim since the last api entry. It will still write to the
    api after X minutes (defined in admin plant settings) even if there is no
    new data. Additionally, it will write the current hours_per_unit statistics if it is
    within 5 minutes of the end of the hour in order to capture a final
    snapshot of the shift.

    Both day and shift hours_per_unit up to that time are written to the API hours_per_unitATM table
    if those conditions are met.

    :return: True if it writes or None and print the reason why it did not
        write.
    """
    # Finds the latest plant settings and pulls the time between writing if no
    # entries are found and the simulated time from the data dripper
    plant_settings = PlantSetting.objects.latest('timestamp')
    now = get_time_with_timezone(plant_settings)

    print("/"*50)
    print("GET NEW hours_per_unit DATA")
    print("/"*50)
    print("NOW TIME = ", now)
    print("TZ: ", now.tzinfo)

    # Checks that there was a claim in the database and does not write if not.
    last_claim = get_last_claim(now)
    if last_claim is None:
        return

    # Checks for the last time an hours_per_unit snapshot was written
    last_api_write, found_entry = get_last_api_write(now)

    # If an entry is found, should we write again?
    # If no entry, it will need to write.
    if found_entry:
        # Is there a new entry, has enough time passed, or is it close to the
        # end of a shift?
        does_need_to_write = need_to_write(now, plant_settings, last_api_write,
                                           last_claim)
        if not does_need_to_write:
            return

    # Call function to calc hours_per_unit by dept for the current shift.
    hours_per_unit_dict = get_hours_per_unit_snap(now)
    # If there is no dictionary returned, or the claims are 0, check other
    # write conditions
    if no_dict_or_no_claims(hours_per_unit_dict):
        # if there was a previous API entry and
        if found_entry and not does_need_to_write:
            print('No hours_per_unit_DICT or no claims in dict. Exiting without write.')
            return

    print("COMPLETED hours_per_unit DICT FROM FORMULAS: ", hours_per_unit_dict)
    print("COMPLETED hours_per_unit DICT CLAIMS_FOR_RANGE: ",
          hours_per_unit_dict['claims_for_range'])

    # Calls functions to calculate values for the day so far and creates a dict
    hours_per_unit_dict_with_day = get_day_hours_per_unit_dict(hours_per_unit_dict, now)

    # Checks if any entries need to be deleted due to age before writing
    delete_old_entries(plant_settings, now)
    write_data(hours_per_unit_dict_with_day)
    print("Wrote data.")
    return True


def write_data(full_hours_per_unit_dict):
    """
    Uses the full dictionary of department and plant hours_per_unit infor for the day to
    write a new entry to the hours_per_unitATM API table.

    :param full_hours_per_unit_dict: Dictionary object with shift and day values for
        departments and plant.
    :return: None
    """
    hours_per_unitATM.objects.create(**full_hours_per_unit_dict)
