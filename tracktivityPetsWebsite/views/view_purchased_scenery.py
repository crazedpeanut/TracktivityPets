from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static 
import fitapp
from tracktivityPetsWebsite import utils
from tracktivityPetsWebsite.models import Scenery
from django.shortcuts import redirect
import fitapp.utils
from django.core import serializers
import json


@login_required
def view_purchased_scenery(request, scenery_index=""):
    '''
    The view_purchased_scenery method finds the scenery that corresponds with the scenery_index parameter.
    The details for the scenery are then returned back to the users browser in JSON format.
    '''

    try:
        scenery = Scenery.objects.get(id=scenery_index) #get the scenery in the url
        name = scenery.name
    except Exception as e: #scenery not found
        return HttpResponse("here " + str(e))
        return redirect('tracktivityPetsWebsite:dashboard') #should probably reverse to take them back to page they were on?

    try:
        owned_scenery = request.user.profile.inventory.collectedscenery_set.get(scenery=scenery) #if user has that scenery in inventory
        owns_scenery = True
    except Exception as e:
        owns_scenery = False
        return HttpResponse(str(e))

    
    if owns_scenery:
        details = {}
        
        try:  #may not own any items
            default_scenery = owned_scenery   

            details['name'] = default_scenery.scenery.name
            details['description'] = default_scenery.scenery.description
            details['image'] = default_scenery.scenery.get_image_path()
            details['pk'] = default_scenery.scenery.pk
        except Exception as e:
            details = str(e)
            
        return HttpResponse(json.dumps(details))
    else:
        return HttpResponse(scenery.name)
