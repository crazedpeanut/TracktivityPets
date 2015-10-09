from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static 
import fitapp
from tracktivityPetsWebsite import utils
from tracktivityPetsWebsite.models import Scenery
import json

@login_required
def set_current_scenery(request, scenery_index=""):
    '''
    The set_current_scenery method, as the name suggests, sets the current scenery for the
    user that was passed in with the request object.
    '''
    if scenery_index is "":
        return HttpResponse("False")
    else:
        try:
            scenery = Scenery.objects.get(id=scenery_index) #get the pet in the url
            owned_scenery = request.user.profile.inventory.collectedscenery_set.get(scenery=scenery) #if user has that pet in inventory
        except:
            return HttpResponse("False")
        if(utils.set_current_scenery(request.user.profile.current_pet, owned_scenery)):
            return HttpResponse("True")
        else:
            return HttpResponse("False")