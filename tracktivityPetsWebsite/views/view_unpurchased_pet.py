from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static 
import fitapp
from tracktivityPetsWebsite import utils
from tracktivityPetsWebsite.models import Pet, Item, CollectedItem, Level
from django.shortcuts import redirect
import fitapp.utils
import json
from tracktivityPetsWebsite import utils


@login_required
def view_unpurchased_pet(request, pet_index=""):
    '''
    The view_unpurchased_pet method finds the pet that corresponds with the pet_index parameter.
    The details for the pet are then returned back to the users browser in JSON format.
    '''

    try:
        pet = Pet.objects.get(id=pet_index) #get the pet in the url
        name = pet.default_name
    except: #pet not found
        return HttpResponse("Pet not found")

    levelOne = Level.objects.get(level=1)

    details = {}
    details['name'] = pet.default_name
    details['cost'] = pet.cost
    details['story'] = "This pet is locked, to unlock you need another " + str(pet.experience_to_unlock - request.user.profile.get_total_xp()) + " experience."
    details['image'] = pet.get_default_image_path()
    details['cost'] = pet.cost
    details['locked'] = 'true'
    
    if request.user.profile.get_total_xp() >= pet.experience_to_unlock:
        details['locked'] = 'false'
        details['story'] = pet.story_set.filter(level_unlocked=levelOne)[0].text
        
    
    return HttpResponse(json.dumps(details))
