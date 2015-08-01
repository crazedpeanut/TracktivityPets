from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static 
import fitapp
from tracktivityPetsWebsite import utils
from tracktivityPetsWebsite.models import Pet, Item, CollectedItem, Level
import json

@login_required
def set_current_pet(request, pet_index=""):
    if pet_index is "":
        return HttpResponse("False")
    else:
        try:
            pet = Pet.objects.get(id=pet_index) #get the pet in the url
            owned_pet = request.user.profile.inventory.collectedpet_set.get(pet=pet) #if user has that pet in inventory
        except:
            return HttpResponse("False")
        if(utils.set_current_pet(request.user, owned_pet)):
            return HttpResponse("True")
        else:
            return HttpResponse("False")