import json

from django.http import HttpResponse
from django.shortcuts import render

from models import Attendee
# Create your views here.


def tracking(request, group_hash):
    context = {'url_root': request.get_host(), 'group_hash': group_hash}
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
