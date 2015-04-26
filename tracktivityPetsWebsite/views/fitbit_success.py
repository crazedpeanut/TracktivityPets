from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

@login_required
def fitbit_success(request):
    return render(request, 'tracktivityPetsWebsite/fitbit_success.html')
