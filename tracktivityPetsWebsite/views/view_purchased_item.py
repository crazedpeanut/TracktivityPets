from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static 
import fitapp
from tracktivityPetsWebsite import utils
from tracktivityPetsWebsite.models import Pet, Item, CollectedItem, Level
from django.shortcuts import redirect
import fitapp.utils
from django.core import serializers
import json


@login_required
def view_purchased_item(request, item_index=""):
    '''
    The view_purchased_item method finds the purchased item that corresponds with the item_index parameter.
    The details for the purchased item are then returned back to the users browser in JSON format.
    '''

    try:
        item = Item.objects.get(id=item_index) #get the item in the url
        name = item.name
    except Exception as e: #pet not found
        return HttpResponse(str(e))
        return redirect('tracktivityPetsWebsite:dashboard') #should probably reverse to take them back to page they were on?

    try:
        owned_item = request.user.profile.inventory.collecteditem_set.get(item=item) #if user has that item in inventory
        owns_item = True
    except Exception as e:
        owns_item = False

    
    if owns_item:
        details = {}
        
        try:  #may not own any items
            default_item = owned_item    

            details['name'] = default_item.item.name
            details['description'] = default_item.item.description
            details['image'] = default_item.item.get_image_path()
            details['pk'] = default_item.item.pk
            details["equipped"] = ("equipped" if default_item.equipped else "not_equipped")
        except Exception as e:
            details = str(e)
            
        return HttpResponse(json.dumps(details))
    else:
        return HttpResponse("")
