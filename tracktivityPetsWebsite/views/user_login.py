from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import fitapp

def user_login(request):
    if  request.user.is_authenticated(): #if user is logged in
        fitbit_synched = False;
        if fitapp.utils.is_integrated(request.user):
            fitbit_synched = True
        
        return render(request, 'tracktivityPetsWebsite/login.html', {"synched": fitbit_synched})
    
    elif request.method == 'POST': #if http request was made with POST type
        try:
            email = request.POST['email'] #get and store username
        except:
            return render(request, 'tracktivityPetsWebsite/splash.html', { "error_message": "No email" })
        
        try:
            password = request.POST['password'] #get and store password
        except:
            return render(request, 'tracktivityPetsWebsite/splash.html', { "error_message": "No password" })
        
        try:
            u = User.objects.get(email=email)
        except:
            return render(request, 'tracktivityPetsWebsite/splash.html', { "error_message": "No user with that email" })   
        
        user = authenticate(username=u.get_username(), password=password) #django method to see if user exists in database
        if user is not None:
            if user.is_active: #if the account is activated
                login(request, user) #log the user into a session
                fitbit_synched = False;
                if fitapp.utils.is_integrated(user):
                    fitbit_synched = True
                return render(request, 'tracktivityPetsWebsite/splash.html', {"synched": fitbit_synched})
            else:
                fitbit_synched = False;
                if fitapp.utils.is_integrated(user):
                    fitbit_synched = True
                return render(request, 'tracktivityPetsWebsite/splash.html')
        else:
            return render(request, 'tracktivityPetsWebsite/splash.html', { "error_message": "Incorrect username/password combination" }) #no user was found
        
    else:
        return render(request, 'tracktivityPetsWebsite/splash.html')