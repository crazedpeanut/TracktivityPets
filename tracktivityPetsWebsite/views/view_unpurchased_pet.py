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


@login_required
def view_unpurchased_pet(request, pet_index=""):

    try:
        pet = Pet.objects.get(id=pet_index) #get the pet in the url
        name = pet.default_name
    except: #pet not found
        return HttpResponse("Pet not found")

    levelOne = Level.objects.get(level=1)

    details = {}
    details['name'] = pet.default_name
    details['cost'] = pet.cost
    details['story'] = pet.story_set.filter(level_unlocked=levelOne)[0].text
    
    return HttpResponse(json.dumps(details))
