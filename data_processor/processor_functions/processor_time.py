from django.utils import timezone


def get_time_with_timezone(plant_settings):
    """
    Gets the current time, making it timezone aware and in US/Eastern.

    :param plant_settings: The most recent instance of the plant settings.
    :return: TZ aware datetime object
    """
    with timezone.override("US/Eastern"):
        return timezone.localtime(plant_settings.dripper_start)
