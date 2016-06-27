from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from .models import hours_per_unitATM
from .views import hours_per_unitAPI
import pytz
import datetime as dt


class hours_per_unitAPITest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()
        User.objects.create(username='cameron', password='password123')

        # Create 2 test objects
        hours_per_unitATM.objects.create(timestamp=pytz.utc.localize(dt.datetime(2016, 6, 1, 10, 30, 0, 0)), hours_per_unit_plant=89.9)

        hours_per_unitATM.objects.create(timestamp=pytz.utc.localize(dt.datetime(2016, 6, 1, 15, 30, 0, 0)), hours_per_unit_plant=86.7)


    def test_list_view(self):
        request = self.factory.get('/api/hours_per_unit')
        user = User.objects.get(username='cameron')
        force_authenticate(request, user='cameron')
        response = hours_per_unitAPI.as_view()(request)

        # Gets 200 response code
        self.assertEqual(response.status_code, 200)
        # Returns only 2 results for 2 items in the table
        self.assertEqual(len(response.data), 2)
        # Returns the correct hours_per_unit when querying the response data
        self.assertEqual(response.data[0]['hours_per_unit_plant'], '89.9')
        self.assertEqual(response.data[1]['hours_per_unit_plant'], '86.7')
