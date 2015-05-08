from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from tracktivityPetsWebsite import utils
import json

@login_required
def pet_selection(request):
    #if user has a current pet redirect away
    
    #NOTE: THE METHOD FOR POST IS TOTALLY UNTESTED
    if request.method == 'POST':
        try:
            pet_name = request.POST.get('user_pet_name', None)
            pet = Pet.objects.filter(default_name=request.POST.get('default_pet_name', None))#pet should be chosen when the user clicks 'select' or whatever, POST the default_name found in the data passed
            if pet_name is None or pet is None:
                return HttpResponse('need to enter all details') 
            success, error = utils.register_pet_selection(request.user, pet, pet_name)
            if success: 
                return HttpResponse('it worked')
            else:
                if error is not None:
                    return HttpResponse(error)
                else:
                    return HttpResponse('You already have a pet, please contact admin')#this should never appear
            
            
        except:
            return HttpResponse('Error creating pet')#shouldnt occur, only if they modify data on their end before sending
    else:
        data = utils.get_pet_selection_data()
        return render(request, 'tracktivityPetsWebsite/pet_selection.html', {'available_pets':data, 'crap':json.dumps(data)}) #this should be a template, just like this for testing purposes