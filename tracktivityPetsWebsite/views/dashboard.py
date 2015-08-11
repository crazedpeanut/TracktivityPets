from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static 
import fitapp
from tracktivityPetsWebsite import utils
from django.shortcuts import redirect
import fitapp.utils
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
hdlr = logging.FileHandler(settings.LOG_LOCATION + '/tracktivitypets_dashboard.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

@login_required
def dashboard(request):
    if not utils.is_fitbit_linked(request.user) or not fitapp.utils.is_integrated(request.user):
       return redirect('tracktivityPetsWebsite:fitbit_link')
    
    elif request.user.profile.current_pet is None:#take them to the page to select a pet
        return redirect('tracktivityPetsWebsite:pet_selection')

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

    happiness_data = current_pet.get_happiness_last_seven_days()
    experience_data = current_pet.get_all_accumulative_experience()
    
    '''try:
        experience_progress = int(round(current_pet.get_total_experience() / experience_needed * 100, 0))
    except:
        experience_progress = 0'''
    
    experience_progress = 0
    progress_bar_text = ""
    progress_bar_colour = ""
    
    if current_pet.level.level == 10:
        experience_progress = 100
        progress_bar_text = "%s has reached maximum level!" % (current_pet.name)
        progress_bar_colour = "progress-bar-success"
    elif current_pet.level.level == 1 and current_pet.get_total_experience() == 0:
        experience_progress = 100
        progress_bar_text = "%s hasn't gained any experience yet." % (current_pet.name)
        progress_bar_colour = "progress-bar-danger"
    else:
        experience_progress = int(round(current_pet.get_total_experience() / experience_needed * 100, 0))
        progress_bar_text = "{total}/ {needed} ({percent}%)".format(total=current_pet.get_total_experience(), needed=experience_needed, percent=experience_progress)
        '''progress_bar_test = "Hello!"'''
        progress_bar_colour = "progress-bar-warning"
        
    happiness_today = current_pet.get_todays_happiness_value()
    level_data = {"progress_bar_text": progress_bar_text, "current_experience": current_pet.get_total_experience(), "experience_to_next_level": experience_needed, "current_level": current_pet.level.level, "progress": experience_progress} #get_current_level()
    
    pet_name = current_pet.name
    
    stories_unlocked = current_pet.get_unlocked_stories()
    stories_available = current_pet.get_stories_available()

    error = ""

    return render(request, 'tracktivityPetsWebsite/dashboard/dashboard.html',  
                  {
                   "pet_name": pet_name,
                   "happiness_graph_data": happiness_data,
                   "experience_graph_data": experience_data,
                   "happiness_today": happiness_today,
                   "mood": mood,
                   "level_data": level_data,
                   "age": age,
                   #"experience_gained": data['experience_gained'],
                   #"levels_gained": data['levels_gained'],
                   "error": error,
                   "stories_unlocked_count": stories_unlocked.count(),
                   "stories_available_count": stories_available.count(),
                   "stories_unlocked": stories_unlocked,
                   #"stories_gained": data['stories'],
                   "progress_bar_colour": progress_bar_colour
                   })