import base64
import csv
import json

from django.db.models import Count
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from functools import wraps

from models import Attendee
from models import Event, EventSerializer
from models import EventAttendance
from models import Group
from models import GroupAdmin
from models import GroupGrades


def authenticate(username, password, group_hash):
    group = Group.objects.filter(group_hash=group_hash)
    if not group:
        return None
    user = GroupAdmin.objects.filter(name=username, password=password, group=group)
    if not user:
        return None
    return user


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        request = args[0]
        group_hash = kwargs['group_hash']

        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == 'basic':
                    username, password = base64.b64decode(auth[1]).split(':')
                    user = authenticate(username, password, group_hash)
                    if user:
                        return f(*args, **kwargs)

        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="%s"' % "Basci Auth Protected"
        response.content = 'UNAUTHORIZED, get the right creds plz'
        return response

    return decorated


@requires_auth
def admin_overview(request, group_hash):
    group = get_object_or_404(Group, group_hash=group_hash)

    events = Event.objects.filter(group_hash=group.group_hash, archived=False).order_by('date')
    counts = EventAttendance.objects.values('event_id').annotate(event_count=Count('event_id'))
    serializable_events = EventSerializer().serialize(events)

    for event in serializable_events:
        for i in counts:
            if i['event_id'] == event['id']:
                event['count'] = i['event_count']

        if 'count' not in event:
            event['count'] = 0

    context = {'name': group.name, 'events': serializable_events,
               'events_json': json.dumps(serializable_events),
               'group_hash': group_hash}
    return render(request, 'admin.html', context)


def csv_download(request, group_hash, event_id):
    group = get_object_or_404(Group, group_hash=group_hash)
    event = get_object_or_404(Event, id=event_id)

    fullArray = []
    fullArray.append([group.name, event.name, event.date, ""])
    fullArray.append(['Name', 'Email', 'Year',  'First Time?'])

    event_attendance = EventAttendance.objects.filter(event_id=event_id).select_related('attendee')
    for record in event_attendance:
        full_name = record.attendee.first_name + " " + record.attendee.last_name

        temp = [full_name.encode('utf-8').strip(), record.attendee.email, record.attendee.year, record.first_time]
        fullArray.append(temp)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + event.name + '-' + str(event.date) + '.csv"'

    writer = csv.writer(response)
    for row in fullArray:
        writer.writerow(row)

    return response


def create_event(request, group_hash):
    group = get_object_or_404(Group, group_hash=group_hash)

    input_name = request.GET.get('name', '')
    if not input_name:
        return HttpResponseBadRequest()

    new_event = Event.objects.create(
        name=input_name,
        group_hash=group_hash,
    )

    serializable_event = EventSerializer().serialize([new_event])

    return redirect('arkaios.views.admin_overview', group_hash=group_hash)


def event_toggle(request, group_hash, event_id):
    group = get_object_or_404(Group, group_hash=group_hash)
    event = get_object_or_404(Event, id=event_id)

    on = request.GET.get('on', 'false').lower()
    on = True if on == 'true' else False

    event.on = on
    event.save()

    results_dict = {
        'event_id': event.id,
        'event_status': event.on
    }

    return HttpResponse(json.dumps(results_dict))


@requires_auth
def tracking(request, group_hash, event_id):
    group = get_object_or_404(Group, group_hash=group_hash)
    event = get_object_or_404(Event, id=event_id)
    grade_options = GroupGrades.objects.filter(group_hash=group_hash)
    context = {'url_root': request.get_host(), 'group_hash': group_hash,
               'event_id': event_id, 'event_name': event.name,
               'grade_options': grade_options, 'group_name': group.name,
               'return_url': 'http://' + request.get_host() + '/arkaios/' + group_hash + '/admin/'}
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
    input_listserv = request.GET.get('listserv', 'true').strip().lower()
    print(input_listserv)

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

        if input_listserv not in ['false', 'true']:
            error_array.append("listserv")

        results_dict['status'] = 'error'
        results_dict['error'] = error_array

        return HttpResponse(json.dumps(results_dict))

    bool_listserv = input_listserv == 'true'

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
            year=input_year,
            email_list=bool_listserv
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

    # update the attendee with the new bool value
    attendee.email_list = bool_listserv
    attendee.save()

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
