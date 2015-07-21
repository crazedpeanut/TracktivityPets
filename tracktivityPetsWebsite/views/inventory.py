from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tracktivityPetsWebsite.models import Item

@login_required
def inventory(request, item_index=""):
    if item_index is "": #ie <site>/inventory/
        
        all_items = Item.objects.all()
        owned_items = request.user.profile.inventory.get_owned_items()
        locked_items = request.user.profile.inventory.calculate_locked_items(all_items, owned_items)
        
        return render(request, 'tracktivityPetsWebsite/inventory.html',  
        {
            "all_items": all_items,
            "owned_items": owned_items,
            "locked_items": locked_items,
        })
    else: #ie <site>/inventory/4/
        return render(request, 'tracktivityPetsWebsite/inventory.html',  
        {
            "view_item": True,
        })
