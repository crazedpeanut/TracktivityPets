from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from tracktivityPetsWebsite.forms import LoginForm
import fitapp

def user_login(request):
    if  request.user.is_authenticated(): #if user is logged in
        fitbit_synched = False;
        if fitapp.utils.is_integrated(request.user):
            fitbit_synched = True
        return render(request, 'tracktivityPetsWebsite/login.html', {"synched": fitbit_synched})
    
    elif(request.method == "GET"):
        loginForm = LoginForm()
        return render(request, 'tracktivityPetsWebsite/splash.html', {'loginForm': loginForm} )
    
    elif(request.method == "POST"): #if http request was made with POST type
        
        loginForm = LoginForm(request.POST)
        
        if(loginForm.is_valid() is not True):
            loginForm = LoginForm()
            return render(request, 'tracktivityPetsWebsite/splash.html', { "error_message": "Form invalid",'loginForm':loginForm})
        else:
            email = loginForm.cleaned_data['email']
            password = loginForm.cleaned_data['password']
            rememberMe = loginForm.cleaned_data['rememberMe']
            u = User.objects.get(email=email)
            
            user = authenticate(username=u.get_username(), password=password)
            
            if(user is not None):
                if(user.is_active):
                    login(request, user)
                    fitbit_synched = False
                    
                    if(fitapp.utils.is_integrated(user)):
                        fitbit_synched = True
                        
                    if(rememberMe):
                        request.session.set_expiry(settings.REMEMBER_ME_DURATION)
                    return render(request, 'tracktivityPetsWebsite/splash.html', {"synched": fitbit_synched})
                else:
                    fitbit_synched = False
                    
                    if(fitapp.utils.is_integrated(user)):
                        fitbit_synched = True
                        return render(request, 'tracktivityPetsWebsite/splash.html')
            else:
                loginForm = LoginForm()
                return render(request, 'tracktivityPetsWebsite/splash.html', { "error_message": "Incorrect username/password combination",'loginForm':loginForm}) #no user was found
                
        
        '''
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
                    
                if request.POST.get('remember-me', False):
                    request.session.set_expiry(settings.REMEMBER_ME_DURATION)
                    
                return render(request, 'tracktivityPetsWebsite/splash.html', {"synched": fitbit_synched})
            else:
                fitbit_synched = False;
                if fitapp.utils.is_integrated(user):
                    fitbit_synched = True
                return render(request, 'tracktivityPetsWebsite/splash.html')
        else:
            loginForm = LoginForm()
            return render(request, 'tracktivityPetsWebsite/splash.html', { "error_message": "Incorrect username/password combination",'loginForm':loginForm}) #no user was found
        
    else:
        loginForm = LoginForm()
        return render(request, 'tracktivityPetsWebsite/splash.html', {'loginForm': loginForm} )
    '''