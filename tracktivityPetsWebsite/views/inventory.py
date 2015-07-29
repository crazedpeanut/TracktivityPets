from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tracktivityPetsWebsite.models import Item, Pet
from tracktivityPetsWebsite import utils

@login_required
def inventory(request, item_index=""):
    if item_index is "": #ie <site>/inventory/
        
        all_items = Item.objects.all()
        collected_items = request.user.profile.inventory.get_owned_items()
        locked_items = request.user.profile.inventory.calculate_unpurchased_items(all_items, collected_items)
        all_pets = Pet.objects.all()
        collected_pets = request.user.profile.inventory.get_owned_pets()
        unpurchased_pets = request.user.profile.inventory.calculate_unpurchased_pets(all_pets, collected_pets) 
        
        
        
        
        return render(request, 'tracktivityPetsWebsite/inventory.html',  
        {
            "collected_pets": collected_pets,
            "unpurchased_pets": unpurchased_pets,
            "collected_items": collected_items,
            "locked_items": locked_items,
        })
    else: #ie <site>/inventory/4/
        return render(request, 'tracktivityPetsWebsite/inventory.html',  
        {
            "view_item": True,
        })
