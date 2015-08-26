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

    try:
        item = Item.objects.get(id=item_index) #get the item in the url
    except: #pet not found
        return HttpResponse("Item not found")

    details = {}
    details['name'] = item.name
    details['cost'] = item.cost
    details['description'] = item.description
    details['image'] = item.get_image_path()
    
    return HttpResponse(json.dumps(details))
