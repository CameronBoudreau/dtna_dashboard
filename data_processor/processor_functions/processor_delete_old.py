from api.models import hours_per_unitATM
import datetime as dt


def delete_old_entries(plant_settings, now):
    """
    Checks settings for desired length of time to keep API entries. Deletes any
    data older than the found value in days.

    :param now: The simulated time - datetime object.
    :param plant_settings: The most recent instance of the plant settings.
    :return: None.
    """
    del_after_date = now - dt.timedelta(days=plant_settings.del_after)
    hours_per_unitATM.objects.filter(timestamp__lte=del_after_date).delete()
