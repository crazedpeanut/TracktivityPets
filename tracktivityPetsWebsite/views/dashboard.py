from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import fitapp

@login_required
def dashboard(request):
    fitbit_synched = False;
    if fitapp.utils.is_integrated(request.user):
        fitbit_synched = True
    return render(request, 'tracktivityPetsWebsite/dashboard.html',  {"synched": fitbit_synched})