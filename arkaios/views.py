import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from models import Attendee
from models import Event
from models import EventAttendance
# Create your views here.


def tracking(request, group_hash, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {'url_root': request.get_host(), 'group_hash': group_hash,
               'event_id': event_id, 'event_name': event.name}
    return render(request, 'largegroup.html', context)


def search(request, group_hash):
    search_dict = {'group_hash': group_hash}
    for key in request.GET:
        if request.GET.get(key, ''):
            updated_key = key + '__icontains'
            search_dict[updated_key] = request.GET.get(key)

    returned_attendees = Attendee.objects.filter(**search_dict)
    results_dict = {"results": []}
    for attendee in returned_attendees:
        temp_dict = {
            "year": attendee.year,
            "firstname": attendee.first_name,
            "lastname": attendee.last_name,
            "email": attendee.email
        }
        results_dict['results'].append(temp_dict)

    return HttpResponse(json.dumps(results_dict))


def save(request, group_hash, event_id):
    results_dict = {'status': 'error'}
    # perform data validation on fields, strip/lower
    input_first_name = request.GET.get('firstName', '').strip().lower()
    input_last_name = request.GET.get('lastName', '').strip().lower()
    input_email = request.GET.get('email', '').strip().lower()
    input_year = request.GET.get('year', '').strip().lower()

    error_array = []
    if ((not input_first_name) or (not input_last_name) or (not input_email)
        or (not input_year)):
        if not input_first_name:
            error_array.append("firstName")

        if not input_last_name:
            error_array.append("lastName")

        if not input_email:
            error_array.append("email")

        if not input_year:
            error_array.append("year")

        results_dict['status'] = 'error'
        results_dict['error'] = error_array

        return HttpResponse(json.dumps(results_dict))

    # make sure that event is valid
    event = Event.objects.filter(id=event_id, on=True)
    if not event:
        results_dict['status'] = 'error'
        results_dict['event'] = 'invalid'

        return HttpResponse(json.dumps(results_dict))
    # look up user in database

    event = event[0]

    attendee = Attendee.objects.filter(group_hash=group_hash, email=input_email)

    # if first time
    if not attendee:

        new_attendee = Attendee.objects.create(
            group_hash=group_hash,
            email=input_email,
            first_name=input_first_name,
            last_name=input_last_name,
            year=input_year
        )

        new_attendance = EventAttendance.objects.create(
            attendee=new_attendee,
            event=event,
            first_time=1
        )

        results_dict['status'] = 'success'
        return HttpResponse(json.dumps(results_dict))

    attendee = attendee[0]
    attendance = EventAttendance.objects.filter(attendee=attendee, event=event)

    if attendance:
        # attendance record already exists, do nothing but return success
        results_dict['status'] = 'success'
        return HttpResponse(json.dumps(results_dict))

    # at this point, an attendee exists, an event exists, but no attendance record
    #   has been created - time to create one!
    new_attendance = EventAttendance.objects.create(
        attendee=attendee,
        event=event,
        first_time=0
    )
    results_dict['status'] = 'success'
    return HttpResponse(json.dumps(results_dict))
