from django.shortcuts import render
from django.http import HttpResponse
from tracktivityPetsWebsite.forms import RegisterForm


#from tracktivityPetsWebsite import utils #example of using utils

def register(request):
    registerForm = RegisterForm()
    #message = utils.register_user('bob', 'brown', 'bob@test.com', 'bobby', 'swagcats', 'swagcats') #example of using register function, message is None if it worked
    return render(request, 'tracktivityPetsWebsite/register.html', {'registerForm': registerForm} )
