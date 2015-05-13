from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static 
import fitapp
from tracktivityPetsWebsite import utils
from django.shortcuts import redirect
import fitapp.utils
import json

@login_required
def dashboard(request):
    
    if not utils.is_fitbit_linked(request.user) or not fitapp.utils.is_integrated(request.user):
        return redirect('/fitbit/login')
    
    elif request.user.profile.current_pet is None:#take them to the page to select a pet
        return redirect('tracktivityPetsWebsite:pet_selection')
        
    success, data = utils.update_user_fitbit(request)
    
    if not success and data == 103:# :103: Fitbit authentication credentials are invalid and have been removed.
        return redirect('/fitbit/login')
        
    start_url = static('tracktivityPetsWebsite/images')
    
    current_pet = utils.get_current_pet(request.user)
    
    current_mood = current_pet.get_current_mood()
    
    phrase = current_pet.get_random_current_phrase_by_mood(current_mood).text
    mood = {"phrase": phrase, "image": '{url}/pets/{name}/{location}'.format(url=start_url, name= current_pet.pet, location=current_mood.image_location)} 
    
    next_level = current_pet.get_next_level()
    if next_level is None:
        experience_needed = 0
    else:
        experience_needed = next_level.experience_needed
    
    age = current_pet.get_age_in_days()
    
    error = "" 
    
    if not success:
        error = data #get the error message
        
        data = {}
        data['experience_gained'] = -1
        data['levels_gained'] = -1
        data['stories'] = ''
    
    happiness_data = current_pet.get_happiness_last_seven_days()#[25, 50, 40, 70, 10, 80, 60]#temp data
    largest_experience, experience_data = current_pet.get_experience_last_seven_days()#[2500, 5000, 4000, 7000, 1000, 8000, 6000]
    
     try:
        experience_progress = int(round(current_pet.get_total_experience() / experience_needed * 100, 0))
    except:
        experience_progress = 0
        
    happiness_today = current_pet.get_todays_happiness_value()
    level_data = {"current_experience": current_pet.get_total_experience(), "experience_to_next_level": experience_needed, "current_level": current_pet.level.level, "progress": experience_progress} #get_current_level()
    
    pet_name = current_pet.name
    
    stories_unlocked = current_pet.get_unlocked_stories()
    stories_available = current_pet.get_stories_available()

    return render(request, 'tracktivityPetsWebsite/dashboard.html',  
                  {
                   "pet_name": pet_name,
                   "happiness_graph_data": happiness_data,
                   "experience_graph_data": experience_data,
                   "happiness_today": happiness_today,
                   "largest_experience": largest_experience,
                   "mood": mood,
                   "level_data": level_data,
                   "age": age,
                   "experience_gained": data['experience_gained'],
                   "levels_gained": data['levels_gained'],
                   "error": error,
                   "stories_unlocked_count": stories_unlocked.count(),
                   "stories_available_count": stories_available.count(),
                   "stories_unlocked": stories_unlocked,
                   "stories_gained": data['stories'],
                   
                   })