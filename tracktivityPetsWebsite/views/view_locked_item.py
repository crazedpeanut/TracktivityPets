from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tracktivityPetsWebsite.models import Item

@login_required
def view_locked_item(request, item_index=""):
    if item_index is "": #ie <site>/item/
        pass
    else: #ie <site>/item/4/
        try:
            item = Item.objects.get(id=item_index)
        except:
            return HttpResponse("Item not found.")
        
        return HttpResponse(item)
