from django.shortcuts import render

# Create your views here.

def tracking(request):
    print "HIZA"
    return render(request, 'largegroup.html')
