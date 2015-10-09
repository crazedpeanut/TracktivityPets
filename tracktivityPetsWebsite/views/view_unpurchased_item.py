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
def view_unpurchased_item(request, item_index=""):
    '''
    The view_unpurchased_item method finds the item that corresponds with the item_index parameter.
    The details for the item are then returned back to the users browser in JSON format.
    '''

    try:
        item = Item.objects.get(id=item_index) #get the item in the url
    except: #pet not found
        return HttpResponse("Item not found")

    details = {}
    details['name'] = item.name
    details['cost'] = item.cost
    details['description'] = "This item is locked, to unlock you need another " + str(item.experience_to_unlock - request.user.profile.get_total_xp()) + " experience."
    details['image'] = item.get_image_path()
    details['locked'] = 'true'
    
    if request.user.profile.get_total_xp() >= item.experience_to_unlock:
        details['locked'] = 'false'
        details['description'] = item.description
        
    return HttpResponse(json.dumps(details))
