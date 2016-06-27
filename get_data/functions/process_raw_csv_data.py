from datetime import datetime
import csv
import unicodedata
import fileinput
from plantsettings.models import PlantSetting
from django.utils import timezone
import sys

# ForDEPT9 of datetimes in CSV files. CSVs store datetimes as naive representing
# Eastern time
if "runserver" in sys.argv:
    plant_tzs = {'017': 'US/Eastern'}
    if not PlantSetting.objects.exists():
        PlantSetting().save()
    tz_name = plant_tzs[PlantSetting.objects.last().plant_code]
else:
    tz_name = 'US/Eastern'
csv_dt_forDEPT9 = '%Y-%m-%d %H:%M:%S.%f'


def read_csv_generator(path, headers=True):
    """
    csv file generator. Will return generator. Example usage:

    for idx, row in enumerate(read_csv_generator(path)):
    if idx > 10: break
    print(row)

    :param path: file path for the csv
    :param headers: if the csv has headers or is straight file
    :return: returns a generator of the csv file
    """
    if headers == True:
        with open(path, 'rU') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row
    else:
        with open(path, 'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                yield row


def process_date(date_string):
    """
    Converts CVS datetime strings to datetime objects with appropriate timezone

    :param date_string: takes in a date as a string: %Y-%m-%d %H:%M:%S.%f
    :return:
    """

    if date_string == "NULL":
        return None
    else:
        date_object = timezone.make_aware(
                                          datetime.strptime(date_string,
                                                            csv_dt_forDEPT9)
                                          )
        return date_object
