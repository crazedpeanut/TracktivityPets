from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

@login_required
def fitbit_success(request):
    '''
    The fitbit_success method sends a message to the Django Fitbit app, 
    so that it can be notified that the user has authorised their account.
    '''
	
    return render(request, 'tracktivityPetsWebsite/fitbit/fitbit_success.html')
