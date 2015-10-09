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
    '''
    The view_unpurchased_scenery method finds the scenery that corresponds with the scenery_index parameter.
    The details for the scenery are then returned back to the users browser in JSON format.
    '''

    try:
        scenery = Scenery.objects.get(id=scenery_index) #get the scenery in the url
    except: #pet not found
        return HttpResponse("Scenery not found")

    details = {}
    details['name'] = scenery.name
    details['cost'] = scenery.cost
    details['description'] = "This scenery is locked, to unlock you need another " + str(scenery.experience_to_unlock - request.user.profile.get_total_xp()) + " experience."
    details['image'] = scenery.get_image_path()
    details['locked'] = 'true'
    
    if request.user.profile.get_total_xp() >= scenery.experience_to_unlock:
        details['description'] = scenery.description
        details['locked'] = 'false'
    
    
    
    return HttpResponse(json.dumps(details))
