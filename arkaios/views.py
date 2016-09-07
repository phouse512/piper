from django.shortcuts import render

# Create your views here.

def tracking(request):
    context= { 'url_root': request.get_host() }
    return render(request, 'largegroup.html', context)
