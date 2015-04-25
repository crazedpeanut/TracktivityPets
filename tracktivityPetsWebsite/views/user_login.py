from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
import fitapp

def user_login(request):
    if  request.user.is_authenticated(): #if user is logged in
        fitbit_synched = False;
        if fitapp.utils.is_integrated(request.user):
            fitbit_synched = True
        return render(request, 'tracktivityPetsWebsite/login.html', {"synched": fitbit_synched})
    
    elif request.method == 'POST': #if http request was made with POST type
        try:
            username = request.POST['username'] #get and store username
        except:
            return render(request, 'tracktivityPetsWebsite/login.html', { "error_message": "No username" })
        
        try:
            password = request.POST['password'] #get and store password
        except:
            return render(request, 'tracktivityPetsWebsite/login.html', { "error_message": "No password" })
        
        user = authenticate(username=username, password=password) #django method to see if user exists in database
        if user is not None:
            if user.is_active: #if the account is activated
                login(request, user) #log the user into a session
                fitbit_synched = False;
                if fitapp.utils.is_integrated(user):
                    fitbit_synched = True
                return render(request, 'tracktivityPetsWebsite/login.html', {"synched": fitbit_synched})
            else:
                fitbit_synched = False;
                if fitapp.utils.is_integrated(user):
                    fitbit_synched = True
                return render(request, 'tracktivityPetsWebsite/login.html')
        else:
            return render(request, 'tracktivityPetsWebsite/login.html', { "error_message": "Incorrect username/password combination" }) #no user was found
        
    else:
        return render(request, 'tracktivityPetsWebsite/login.html')