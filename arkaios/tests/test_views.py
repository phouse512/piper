import json

from django.test import SimpleTestCase
from django.test.client import RequestFactory
from mock import MagicMock
from mock import patch

from arkaios.models import Event
from arkaios.views import admin_overview
from arkaios.views import save


class AdminTests(SimpleTestCase):

    def setUp(self):
        self.rf = RequestFactory()

        self.group_hash = "test"

    @patch('arkaios.views.get_object_or_404')
    @patch('arkaios.views.Event')
    @patch('arkaios.views.authenticate')
    @patch('arkaios.views.base64.b64decode')
    def test_existing_group(self, base64_patch, auth_patch, event_patch, get_object_patch):
        request = self.rf.get('/arkaios/test/admin/', HTTP_AUTHORIZATION="basic test:hi")

        event1 = Event(id=1, name="test", group_hash="wot", on=True)

        get_object_patch.return_value = MagicMock()
        auth_patch.return_value = "hi"
        base64_patch.return_value = "test:hi"
        event_patch.objects.filter.order_by.return_value = [event1]

        response = admin_overview(request, group_hash=self.group_hash)

        self.assertEqual(200, response.status_code)


class SaveAttendanceTests(SimpleTestCase):

    def setUp(self):
        self.rf = RequestFactory()

        self.attendee_mock = MagicMock(name="attendee_mock")
        self.event_mock = MagicMock(name="event_mock")
        self.event_attendance_mock = MagicMock(name="eventAttendance_mock")

    def test_save_no_params(self):
        group_hash = "test"
        event_id = 1
        request = self.rf.get('/arkaios/test/track/1/save/')

        response = save(request, group_hash, event_id)
        json_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual("error", json_response['status'])
        self.assertEqual(["firstName", "lastName", "email", "year"],
                         json_response['error'])

    def test_save_some_params(self):
        group_hash = "test"
        event_id = 1
        request = self.rf.get('/arkaios/test/track/1/save/?firstName=phil&lastName=house')

        response = save(request, group_hash, event_id)
        json_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual("error", json_response['status'])
        self.assertEqual(["email", "year"], json_response['error'])

    @patch('arkaios.views.Event')
    def test_invalid_event_invalid_params(self, event_patch):
        group_hash = "test"
        event_id = 1
        request = self.rf.get('/arkaios/test/track/1/save/?firstName=phil&lastName=house&email=phil&year=senior')

        event_patch.objects.filter.return_value = []

        response = save(request, group_hash, event_id)
        json_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual("error", json_response['status'])
        self.assertEqual("invalid", json_response['event'])

    @patch('arkaios.views.Event')
    @patch('arkaios.views.Attendee')
    @patch('arkaios.views.EventAttendance')
    def test_new_attendee(self, attendance_patch, attendee_patch, event_patch):
        group_hash = "test"
        event_id = 1
        request = self.rf.get('/arkaios/test/track/1/save/?firstName=phil&lastName=house&email=phil&year=senior')

        event_patch.objects.filter.return_value = [self.event_mock]
        attendee_patch.objects.filter.return_value = []

        attendee_patch.objects.create.return_value = self.attendee_mock
        attendance_patch.objects.create.return_value = MagicMock()

        response = save(request, group_hash, event_id)
        json_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual("success", json_response['status'])

        attendance_patch.objects.create.assert_called_once_with(
            attendee=self.attendee_mock,
            event=self.event_mock,
            first_time=1
        )

    @patch('arkaios.views.Event')
    @patch('arkaios.views.Attendee')
    @patch('arkaios.views.EventAttendance')
    def test_existing_attendance(self, attendance_patch, attendee_patch, event_patch):
        group_hash = "test"
        event_id = 1
        request = self.rf.get('/arkaios/test/track/1/save/?firstName=phil&lastName=house&email=phil&year=senior')

        event_patch.objects.filter.return_value = [self.event_mock]
        attendee_patch.objects.filter.return_value = [self.attendee_mock]
        attendance_patch.objects.filter.return_value = [self.event_attendance_mock]

        response = save(request, group_hash, event_id)
        json_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual("success", json_response['status'])

        attendance_patch.objects.create.assert_not_called()
        attendee_patch.objects.create.assert_not_called()

    @patch('arkaios.views.Event')
    @patch('arkaios.views.Attendee')
    @patch('arkaios.views.EventAttendance')
    def test_new_attendance_existing_user(self, attendance_patch, attendee_patch, event_patch):
        group_hash = "test"
        event_id = 1
        request = self.rf.get('/arkaios/test/track/1/save/?firstName=phil&lastName=house&email=phil&year=senior')

        event_patch.objects.filter.return_value = [self.event_mock]
        attendee_patch.objects.filter.return_value = [self.attendee_mock]
        attendance_patch.objects.filter.return_value = []

        response = save(request, group_hash, event_id)
        json_response = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual("success", json_response['status'])

        attendee_patch.objects.create.assert_not_called()
        attendance_patch.objects.create.assert_called_once_with(
            attendee=self.attendee_mock,
            event=self.event_mock,
            first_time=0
        )

