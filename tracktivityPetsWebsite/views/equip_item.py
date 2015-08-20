from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from tracktivityPetsWebsite import utils
from tracktivityPetsWebsite.models import CollectedItem, Item

@login_required
def equip_item(request, item_index="", equip=""):
    if item_index == "":
        return HttpResponse("No item provided.");
    #check if they own that item
    try:
        item = Item.objects.get(id=item_index)
        owned_by_pet = request.user.profile.inventory.is_item_owned_by_pet(request.user.profile.current_pet.pet, item)
        if not owned_by_pet:
            return HttpResponse("Pet does not own this item");
        
    except Exception as e:
        return HttpResponse(str(e));
    
    if equip == "equip": #override equips
        collected_item = CollectedItem.objects.get(item=item)
        utils.equip_item(request.user.profile.current_pet, collected_item, item.body_part)
        return HttpResponse("Item equipped successfully")
    else:
        equipped = utils.is_item_on_bodypart(item.body_part, request.user.profile.current_pet)
        if equipped:
            return HttpResponse("Item equipped on that bodypart already")
        else:
            return HttpResponse("Item not already on that body part")    
