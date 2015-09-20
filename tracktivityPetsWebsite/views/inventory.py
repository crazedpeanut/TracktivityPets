from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tracktivityPetsWebsite.models import Item, Pet, Level
from tracktivityPetsWebsite import utils
from django.http import HttpResponse
import json

@login_required
def inventory(request, tab=""):
    if tab == "" or tab == "pets": #(tab == "pets" and request.is_ajax()): #ie <site>/inventory/
        
        #all_items = Item.objects.all()
        
        #locked_items = request.user.profile.inventory.calculate_unpurchased_items(all_items, collected_items)
        #all_pets = Pet.objects.all()
        collected_pets = request.user.profile.inventory.get_owned_pets()
        #unpurchased_pets = request.user.profile.inventory.calculate_unpurchased_pets(all_pets, collected_pets) 
        
        pets = {}
        
        for collected_pet in collected_pets:
            current_mood = collected_pet.get_current_mood()
            image = utils.generate_pet_image_url(collected_pet.pet, current_mood.image_location)
            pets[collected_pet.name] = {}
            
            pets[collected_pet.name]["pk"] = collected_pet.pet.pk #pk is used in the html to get the Pet not the CollectedPet, so this fixes that
            pets[collected_pet.name]["image"] = image
            
            
        collected_items = request.user.profile.inventory.get_current_pet_owned_items()

        items = {}
        
        try: 
            for collected_item in collected_items:
                items[collected_item.item.name] = {}
                
                items[collected_item.item.name]["pk"] = collected_item.item.pk
                items[collected_item.item.name]["image"] = collected_item.item.get_image_path()    
        except:
            pass
            
        collected_scenery = request.user.profile.inventory.get_owned_scenery()
          
        scenery = {}
        counter = 0
        for s in collected_scenery:
            counter += 1
            image = s.scenery.get_image_path()
            scenery[s.scenery.name] = {}
            
            scenery[s.scenery.name]["pk"] = s.scenery.pk
            scenery[s.scenery.name]["image"] = image    
        
        #below is for default details for pet (which is first to be shown)
        default_pet = collected_pets[0]
        experience = default_pet.get_total_experience()
        level = default_pet.level.level
        levelOne = Level.objects.get(level=1)
        current_mood = default_pet.get_current_mood()
        image_location = current_mood.image_location
        
        details_pet = {}
        details_pet['name'] = default_pet.name
        details_pet['experience'] = experience
        details_pet['level'] = level
        details_pet['story'] = default_pet.pet.story_set.filter(level_unlocked=levelOne)[0].text
        details_pet['image'] = utils.generate_pet_image_url(default_pet.pet, image_location)
        details_pet['age'] = default_pet.get_age_in_days()
        details_pet['pk'] = default_pet.pet.pk
        
        details_item = {}
        
        try:  #may not own any items
            default_item = collected_items[0]    

            details_item['name'] = default_item.item.name
            details_item['description'] = default_item.item.description
            details_item['image'] = default_item.item.get_image_path()
            details_item['pk'] = default_item.item.pk
            details_item["equipped"] = ("Equipped" if default_item.equipped else "Not Equipped")
        except Exception as e:
            details_item = {}
            
        details_scenery = {}
        
        try:  #may not own any items
            default_scenery = collected_scenery[0]   

            details_scenery['name'] = default_scenery.scenery.name
            details_scenery['description'] = default_scenery.scenery.description
            details_scenery['image'] = default_scenery.scenery.get_image_path()
            details_scenery['pk'] = default_scenery.scenery.pk
        except Exception as e:
            default_scenery = {}
        
        if tab == "":
            return render(request, 'tracktivityPetsWebsite/inventory/inventory.html',  
            {
                "collected_pets": pets,
                "collected_items": items,
                "is_items": len(items) > 0,
                "collected_scenery": scenery,
                "default_pet": details_pet,
                "default_item": details_item,
                "default_scenery": details_scenery,
            })
        if tab == "pets":
            data = '{ "collected": ' + json.dumps(pets) + ', "details": ' + json.dumps(details) + ' }'
            
            return HttpResponse(data)

    elif tab == "scenery": # and request.is_ajax():
        return HttpResponse("scenery")
    
    elif tab == "cosmetics": # and request.is_ajax():

           

        return HttpResponse(data)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
