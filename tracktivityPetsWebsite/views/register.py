from django.shortcuts import render
from django.http import HttpResponse
#from tracktivityPetsWebsite import utils #example of using utils

def register(request):
    #message = utils.register_user('bob', 'brown', 'bob@test.com', 'bobby', 'swagcats', 'swagcats') #example of using register function, message is None if it worked
    pass
    return render(request, 'tracktivityPetsWebsite/register.html')
