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
    
    equipped = utils.is_item_on_bodypart(item.body_part, request.user.profile.current_pet)
    if equipped and equip=="":
        return HttpResponse("already_equipped") #otherwise return that it is equipped
    elif not equipped and equip=="":
        equip = "equip" #just equip it, dont need a confirmation
 
    if equip == "unequip": #if user wants to unequip
        collected_item = CollectedItem.objects.get(item=item)
        collected_item.equipped = False
        collected_item.save()
        return HttpResponse("success")  
    elif equip == "equip": #override equips
        collected_item = CollectedItem.objects.get(item=item)
        utils.equip_item(request.user.profile.current_pet, collected_item, item.body_part)
        return HttpResponse("success")
        
