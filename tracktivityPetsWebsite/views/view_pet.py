from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static 
import fitapp
from tracktivityPetsWebsite import utils
from tracktivityPetsWebsite.models import Pet, Item
from django.shortcuts import redirect
import fitapp.utils
import json


@login_required
def view_pet(request, pet_index=""):

    #if user owns pet or not
        #experience
        #level
        #list of usable items
        #rename pet
        #make active
    #else
        #purchase pet with pennies
        
    if pet_index is "":
        owned_pet = request.user.profile.current_pet
        owns_pet = True
        name = owned_pet.name
    else:
        try:
            pet = Pet.objects.get(id=pet_index) #get the pet in the url
            name = pet.default_name
        except: #pet not found
            return redirect('tracktivityPetsWebsite:dashboard') #should probably reverse to take them back to page they were on?
    
        try:
            owned_pet = request.user.profile.inventory.collectedpet_set.get(pet=pet) #if user has that pet in inventory
            owns_pet = True
        except Exception as e:
            owns_pet = False

    
    if owns_pet:
        #use owned_pet, and they are unlocked
        experience = owned_pet.get_total_experience()
        level = owned_pet.level.level
        usable_items = [1, 2, 3]
        
        try: #usable items
            #usable_items = Item.usableon_set.filter(pet_usable_on=owned_pet.pet)
            pass
        except Exception as e:
            #usable_items = str(e)
            pass
        
        return render(request, 'tracktivityPetsWebsite/view_pet.html',  
        {
           "owns_pet": owns_pet,
           "experience": experience,
           "level": level,
           "usable_items": usable_items,
        })
    else:
        #use pet, and they are locked
        cost = 0
        return render(request, 'tracktivityPetsWebsite/view_pet.html',  
        {
           "owns_pet": owns_pet,
           "cost": cost,
        })
