from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from tracktivityPetsWebsite.forms import RegisterForm
from tracktivityPetsWebsite import utils
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

#from tracktivityPetsWebsite import utils #example of using utils

def register(request):
    if request.user.is_authenticated(): #if user is logged in
        return redirect('tracktivityPetsWebsite:dashboard') #go to dashboard
    
    if request.method == "GET":
        registerForm = RegisterForm()
        return render(request, 'tracktivityPetsWebsite/register.html', {'registerForm': registerForm} )
    
    if request.method == "POST":
        registerForm = RegisterForm(request.POST)
        
        if registerForm.is_valid() == False:
            return HttpResponseRedirect(reverse('tracktivityPetsWebsite:user_login')) #Form not valid
        else:
            result = utils.register_user(registerForm=registerForm)
            if result is not None:
                return HttpResponse("User registration didn't work" + result)
            else:
                username = registerForm.cleaned_data['username']
                password = registerForm.cleaned_data['password']
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('tracktivityPetsWebsite:pet_selection') #go to pet_selection
            
        