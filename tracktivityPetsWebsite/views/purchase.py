from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tracktivityPetsWebsite.models import Item, CollectedItem, Scenery, CollectedScenery, Pet, CollectedPet, Level, Profile
from tracktivityPetsWebsite import utils
from django.http import HttpResponse
import json
import datetime

@login_required
def purchase(request, tab="", index=""):
    if tab == "pet": #(tab == "pets" and request.is_ajax()): #ie <site>/inventory/
        #return HttpResponse("True")
        try:
            pet = Pet.objects.get(pk=index)
            try:
                collected_pet = CollectedPet.objects.get(pet=pet)
                return HttpResponse("False") #user already owns the pet, so cant buy again
            except:
                pass
            
            if (request.user.profile.total_pet_pennies >= pet.cost) and request.user.profile.get_total_xp() >= pet.experience_to_unlock:
                name = pet.default_name #change this later to what the user has named it?
                level = Level.objects.get(level=1) #dodgy code, but can presume level 1 will always exist
                now = datetime.datetime.now()
                profile = request.user.profile
                collected_scenery = CollectedScenery.objects.all().order_by('?')[0] #pet starts with random collected scenery
            
                collected_pet = CollectedPet.objects.create(pet=pet, inventory=profile.inventory, level=level, name=name, date_created=now, scenery=collected_scenery) #create new collected pet
                collected_pet.save()
                profile.total_pet_pennies -= pet.cost
                profile.save()
                
                return HttpResponse("True")
            else:
                return HttpResponse("False")
        except:
            return HttpResponse("False")
    elif tab == "scenery": # and request.is_ajax():
        #return HttpResponse("True") #uncomment for testing jquery stuff
        try:
            scenery = Scenery.objects.get(pk=index)
            try:
                collected_scenery = CollectedScenery.objects.get(scenery=scenery)
                return HttpResponse("False") #user already owns the scenery, so cant buy again
            except:
                pass
            
            if (request.user.profile.total_pet_pennies >= scenery.cost) and request.user.profile.get_total_xp() >= scenery.experience_to_unlock:
                
                collected_scenery = CollectedScenery.objects.create(scenery=scenery, inventory=request.user.profile.inventory)
                collected_scenery.save()
                request.user.profile.total_pet_pennies -= scenery.cost
                request.user.profile.save()
                
                return HttpResponse("True")
            else:
                return HttpResponse("False")
        except:
            return HttpResponse("False")
    
    elif tab == "item": # and request.is_ajax():
        #return HttpResponse("True") #uncomment for testing jquery stuff
        try:
            item = Item.objects.get(pk=index)
            try:
                collected_item = CollectedItem.objects.get(item=item)
                return HttpResponse("False") #user already owns the item, so cant buy again
            except:
                pass
            
            if (request.user.profile.total_pet_pennies >= item.cost) and request.user.profile.current_pet.get_total_xp() >= item.experience_to_unlock:
                
                collected_item = CollectedItem.objects.create(item=item, inventory=request.user.profile.inventory)
                collected_item.save()
                request.user.profile.total_pet_pennies -= item.cost
                request.user.profile.save()
                
                return HttpResponse("True")
            else:
                return HttpResponse("False")
        except:
            return HttpResponse("False")
    else:     
        return HttpResponse("False")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
