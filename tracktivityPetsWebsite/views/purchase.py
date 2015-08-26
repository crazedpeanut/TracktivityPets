from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tracktivityPetsWebsite.models import Item, CollectedItem
from tracktivityPetsWebsite import utils
from django.http import HttpResponse
import json

@login_required
def purchase(request, tab="", index=""):
    if tab == "pet": #(tab == "pets" and request.is_ajax()): #ie <site>/inventory/
        #collected_pet = CollectedPet.objects.create(pet=pet, inventory=profile.inventory, level=level, name=name, date_created=now, scenery=collected_scenery) #create new collected pet
        #collected_pet.save()
        return HttpResponse("pets")
    elif tab == "scenery": # and request.is_ajax():
        return HttpResponse("scenery" + index)
    
    elif tab == "item": # and request.is_ajax():
        #return HttpResponse("True")
        try:
            item = Item.objects.get(pk=index)
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
