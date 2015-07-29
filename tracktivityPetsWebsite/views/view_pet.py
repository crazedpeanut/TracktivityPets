from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tracktivityPetsWebsite.models import Pet
from django.shortcuts import redirect


@login_required
def view_pet(request, pet_index=""):

    #if user owns pet or not
        #experience
        #level
        #list of usable items
        #rename pet -- this requires a POST, could ajax it
        #make active
    #else
        #purchase pet with pennies
        
    if pet_index is "": #ie <site>/view_pet/
        owned_pet = request.user.profile.current_pet
        owns_pet = True
        name = owned_pet.name
    else: #ie <site>/view_pet/4/
        try:
            pet = Pet.objects.get(id=pet_index) #get the pet in the url
            name = pet.default_name
        except: #pet not found
            return redirect('tracktivityPetsWebsite:dashboard') #should probably reverse to take them back to page they were on?
    
        try:
            owned_pet = request.user.profile.inventory.collectedpet_set.get(pet=pet) #if user has that pet in inventory
            owns_pet = True
        except Exception as e:
            owns_pet = False

    pet_pennies = request.user.profile.total_pet_pennies
    
    if owns_pet:
        #use owned_pet, and they are unlocked
        experience = owned_pet.get_total_experience()
        level = owned_pet.level.level
        usable_items = owned_pet.get_usable_items()
        owned_items = request.user.profile.inventory.get_owned_items_in_queryset(usable_items)
        
        usable_items = set(usable_items)
        locked_items = request.user.profile.inventory.calculate_locked_items(usable_items, owned_items)
        
        return render(request, 'tracktivityPetsWebsite/view_pet.html',  
        {
           "owns_pet": owns_pet,
           "experience": experience,
           "level": level,
           "usable_items": usable_items,
           "owned_items": owned_items,
           "locked_items": locked_items,
           "pet_pennies": pet_pennies,
        })
    else:
        #use pet, and they are locked
        cost = pet.cost
        return render(request, 'tracktivityPetsWebsite/view_pet.html',  
        {
           "owns_pet": owns_pet,
           "cost": cost,
           "pet_pennies": pet_pennies,
        })
