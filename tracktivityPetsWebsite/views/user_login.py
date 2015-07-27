from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from tracktivityPetsWebsite.forms import LoginForm
from django.shortcuts import redirect
import fitapp

def user_login(request):
    if  request.user.is_authenticated(): #if user is logged in
        return redirect('tracktivityPetsWebsite:dashboard') #go to dashboard
    
    elif request.method == "GET":
        loginForm = LoginForm()
        return render(request, 'tracktivityPetsWebsite/splash.html', {'loginForm': loginForm} )
    
    elif request.method == "POST": #if http request was made with POST type
        
        loginForm = LoginForm(request.POST)
        
        if loginForm.is_valid() is not True:
            loginForm = LoginForm()
            return render(request, 'tracktivityPetsWebsite/splash.html', { "error_message": "Form invalid",'loginForm':loginForm})
        else:
            email = loginForm.cleaned_data['email'].lower()
            password = loginForm.cleaned_data['password']
            rememberMe = loginForm.cleaned_data['rememberMe']
            
            try:
                u = User.objects.get(email=email)
            except:
                return render(request, 'tracktivityPetsWebsite/splash.html', { "error_message": "Incorrect email/password combinatione",'loginForm':loginForm})
            
            user = authenticate(username=u.get_username().lower(), password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    fitbit_synched = False
                    
                    if fitapp.utils.is_integrated(user):
                        fitbit_synched = True
                        
                    if rememberMe:
                        request.session.set_expiry(settings.REMEMBER_ME_DURATION)
                    return redirect('tracktivityPetsWebsite:dashboard')#return render(request, 'tracktivityPetsWebsite/splash.html', {"synched": fitbit_synched})
                else:
                    fitbit_synched = False
                    
                    if fitapp.utils.is_integrated(user):
                        fitbit_synched = True
                        return render(request, 'tracktivityPetsWebsite/splash.html')
            else:
                loginForm = LoginForm()
                return render(request, 'tracktivityPetsWebsite/splash.html', { "error_message": "Incorrect email/password combination",'loginForm':loginForm}) #no user was found
                