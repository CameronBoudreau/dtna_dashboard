from django.test import TestCase
from get_data.models import PlantActivityModel
from django.utils import timezone
import datetime as dt

from data_processor.functions.claims_calculations import get_claimed_objects_in_range, get_range_of_claims

class ClaimData(TestCase):
    def setUp(self):
        #################################################
        # claim trucks previous day as test manhours
        #################################################
        PlantActivityModel.objects.create(
            UNIT_NUM='HZ3849',
            UNIT_COMPLETED_DEPT='03',
            UNIT_LOADED_TIME=timezone.make_aware(dt.datetime(2016, 6, 2, 12, 25)),
        )

        PlantActivityModel.objects.create(
            UNIT_NUM='HZ3850',
            UNIT_COMPLETED_DEPT='03',
            UNIT_LOADED_TIME=timezone.make_aware(dt.datetime(2016, 6, 2, 14, 25)),
        )

        #################################################
        # claim trucks same day as test manhours
        #################################################
        PlantActivityModel.objects.create(
            UNIT_NUM='HZ3851',
            UNIT_COMPLETED_DEPT='DL',
            UNIT_LOADED_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 45)),
        )

        PlantActivityModel.objects.create(
            UNIT_NUM='HZ3852',
            UNIT_COMPLETED_DEPT='03',
            UNIT_LOADED_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 6, 55)),
        )

        PlantActivityModel.objects.create(
            UNIT_NUM='HZ3853',
            UNIT_COMPLETED_DEPT='01',
            UNIT_LOADED_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 7, 15)),
        )

        PlantActivityModel.objects.create(
            UNIT_NUM='HZ3854',
            UNIT_COMPLETED_DEPT='03',
            UNIT_LOADED_TIME=timezone.make_aware(dt.datetime(2016, 6, 3, 8, 15)),
        )

    def test_get_claim_data(self):
        #regular test case of start to end time
        start = timezone.make_aware(dt.datetime(2016, 6, 3, 6, 30))
        stop = timezone.make_aware(dt.datetime(2016, 6, 3, 10, 30))
        num_trucks = get_range_of_claims(start, stop)
        self.assertEqual(num_trucks, 2)

        #testing range
        start = timezone.make_aware(dt.datetime(2016, 6, 2, 6, 30))
        stop = timezone.make_aware(dt.datetime(2016, 6, 3, 7, 30))
        num_trucks = get_range_of_claims(start, stop)
        # print("*"*50)
        # print(num_trucks)
        self.assertEqual(num_trucks, 3)

        claimed_objects = get_claimed_objects_in_range(start, stop)
        expected_claims = ['HZ3849', 'HZ3850', 'HZ3852', 'HZ3854']
        not_expected_claims = ['HZ3854', 'HZ3853']

        for claim in claimed_objects:
            print(claim.UNIT_NUM)
            self.assertIn(claim.UNIT_NUM, expected_claims)
            self.assertNotIn(claim.UNIT_NUM, not_expected_claims)