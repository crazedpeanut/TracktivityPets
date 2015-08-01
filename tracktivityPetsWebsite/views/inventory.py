from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tracktivityPetsWebsite.models import Item, Pet, Level
from tracktivityPetsWebsite import utils
from django.http import HttpResponse
import json

@login_required
def inventory(request, item_index=""):
    if item_index is "": #ie <site>/inventory/
        
        #all_items = Item.objects.all()
        collected_items = request.user.profile.inventory.get_owned_items()
        #locked_items = request.user.profile.inventory.calculate_unpurchased_items(all_items, collected_items)
        #all_pets = Pet.objects.all()
        collected_pets = request.user.profile.inventory.get_owned_pets()
        #unpurchased_pets = request.user.profile.inventory.calculate_unpurchased_pets(all_pets, collected_pets) 
        
        collected = {}
        
        for collected_pet in collected_pets:
            current_mood = collected_pet.get_current_mood()
            image = utils.generate_pet_image_url(collected_pet.pet, current_mood.image_location)
            collected[collected_pet.name] = {}
            
            collected[collected_pet.name]["pk"] = collected_pet.pet.pk #pk is used in the html to get the Pet not the CollectedPet, so this fixes that
            collected[collected_pet.name]["image"] = image
        
        #below is for default details
        default_pet = collected_pets[0]
        experience = default_pet.get_total_experience()
        level = default_pet.level.level
        levelOne = Level.objects.get(level=1)
        current_mood = default_pet.get_current_mood()
        image_location = current_mood.image_location
        
        details = {}
        details['name'] = default_pet.name
        details['experience'] = experience
        details['level'] = level
        details['story'] = default_pet.pet.story_set.filter(level_unlocked=levelOne)[0].text
        details['image'] = utils.generate_pet_image_url(default_pet.pet, image_location)
        details['age'] = default_pet.get_age_in_days()
        
        #return HttpResponse(json.dumps(collected))
        return render(request, 'tracktivityPetsWebsite/inventory.html',  
        {
            "collected_pets": collected,
            "collected_items": collected_items,
            "default": details,
        })
    else: #ie <site>/inventory/4/
        return render(request, 'tracktivityPetsWebsite/inventory.html',  
        {
            "view_item": True,
        })
