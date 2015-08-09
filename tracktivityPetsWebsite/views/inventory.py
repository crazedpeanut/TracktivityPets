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
            
            
        collected_items = request.user.profile.inventory.get_owned_items()
        
        items = {}
        
        for collected_item in collected_items:
            image = "TODO"
            items[collected_item.item.name] = {}
            
            items[collected_item.item.name]["pk"] = collected_item.item.pk
            items[collected_item.item.name]["image"] = image    
           
            
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
        
        details = {}
        details['name'] = default_pet.name
        details['experience'] = experience
        details['level'] = level
        details['story'] = default_pet.pet.story_set.filter(level_unlocked=levelOne)[0].text
        details['image'] = utils.generate_pet_image_url(default_pet.pet, image_location)
        details['age'] = default_pet.get_age_in_days()
        details['pk'] = default_pet.pet.pk
        
        ''' #code for default item if need it
        details = {}
        
        try:  #may not own any items
            default_item = collected_items[0]    

            details['name'] = default_item.item.name
            details['description'] = "Items havent been given a description yet"
            details['image'] = "TODO"
            details['pk'] = default_item.item.pk
            details["equipped_on"] = default_item.equipped_on
        except Exception as e:
            details = str(e)
        
        data = '{ "collected": ' + json.dumps(collected) + ', "details": ' + json.dumps(details) + ' }'
        '''
        
        if tab == "":
            return render(request, 'tracktivityPetsWebsite/inventory/inventory.html',  
            {
                "collected_pets": pets,
                "collected_items": items,
                "collected_scenery": scenery,
                "default": details,
            })
        if tab == "pets":
            data = '{ "collected": ' + json.dumps(pets) + ', "details": ' + json.dumps(details) + ' }'
            
            return HttpResponse(data)

    elif tab == "scenery": # and request.is_ajax():
        return HttpResponse("scenery")
    
    elif tab == "cosmetics": # and request.is_ajax():

           

        return HttpResponse(data)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
