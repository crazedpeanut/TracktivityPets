from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tracktivityPetsWebsite.models import CollectedItem, Item
from django.core import serializers

@login_required
def view_unlocked_item(request, item_index=""):
    if item_index is "": #ie <site>/item/
        
        pass
    else: #ie <site>/item/4/
        try:
            item = CollectedItem.objects.get(id=item_index, inventory=request.user.profile.inventory)
        except:
            return HttpResponse("Item not found.")
        
        return HttpResponse(serializers.serialize("json", [item,]))
