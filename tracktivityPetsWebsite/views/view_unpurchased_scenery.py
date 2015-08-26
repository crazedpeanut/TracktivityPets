from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static 
import fitapp
from tracktivityPetsWebsite import utils
from tracktivityPetsWebsite.models import Scenery
from django.shortcuts import redirect
import fitapp.utils
import json


@login_required
def view_unpurchased_scenery(request, scenery_index=""):

    try:
        scenery = Scenery.objects.get(id=scenery_index) #get the scenery in the url
    except: #pet not found
        return HttpResponse("Scenery not found")

    details = {}
    details['name'] = scenery.name
    details['cost'] = scenery.cost
    details['description'] = scenery.description
    details['image'] = scenery.get_image_path()
    
    return HttpResponse(json.dumps(details))
