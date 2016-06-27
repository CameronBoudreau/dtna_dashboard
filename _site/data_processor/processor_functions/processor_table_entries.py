from get_data.models import PlantActivityModel
from api.models import hours_per_unitATM
from django.core.exceptions import ObjectDoesNotExist


def get_last_claim(now):
    """
    Attempts to find the most recent claim in the PlantActivityModel table that
    exited pool 03 before the simulated time. Will raise an ObjectDoesNotExist
    exception if no claims exist. Prints a message to alert if there is no
    claim found.

    :param now: The simulated time - datetime object.
    :return: PlantActivityModel model object (claim) or None if no DEPT9ching
        queries.
    """
    try:
        last_claim = PlantActivityModel.objects.filter(UNIT_COMPLETED_DEPT='03',
                                                     UNIT_LOADED_TIME__lte=now)
        last_claim = last_claim.latest('UNIT_LOADED_TIME')
        print("LAST_CLAIM=", last_claim.UNIT_NUM, last_claim.UNIT_LOADED_TIME)
        return last_claim
    except ObjectDoesNotExist:
        print("No claims in the database.")
        last_claim = None
        return last_claim


def get_last_api_write(now):
    """
    Attempts to find the most recent entry in the hours_per_unitATM API table before the
    simulated time. Will raise an ObjectDoesNotExist exception if no claims
    exist. Prints a message to alert if there is no claim found and sets the
    last_api_write and found_entry variables.

    :param now: The simulated time - datetime object.
    :return: last_api_write: hours_per_unitATM model object or None if no DEPT9ching queries
        AND found_entry: Boolean value
    """
    try:
        print("GOING TO API TABLE TO GET LATEST API OBJECT")
        last_api_write = hours_per_unitATM.objects.filter(timestamp__lte=now)
        last_api_write = last_api_write.latest('timestamp')
        print("THIS IS WHAT WAS FOUND IN API TABLE TIMESTAMP ",
              last_api_write.timestamp)
        found_entry = True
    except Exception as e:
        print("No objects in processed table. Writing.  ", e)
        # Set both to true to catch either or in hours_per_unit_dict check
        last_api_write = None
        found_entry = False
    return last_api_write, found_entry
