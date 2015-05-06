from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
import fitapp
from tracktivityPetsWebsite import utils

@login_required
def dashboard(request):
    
    if request.user.profile.current_pet is None:
        return HttpResponse('You have no pet!')#TODO: this shouldnt ever actually occur
    
    fitbit_synched = False;
    if fitapp.utils.is_integrated(request.user):
        fitbit_synched = True
        
    data = utils.update_user_fitbit(request)
        
    start_url = static('tracktivityPetsWebsite/images')
    mood = {"phrase": "I'm so happy", "image": '{url}/pets/{name}/{location}" />'.format(url=start_url, name='Melvin', location='happyface.png')} 
    
    next_level = request.user.profile.current_pet.get_next_level()
    if next_level is None:
        experience_needed = 0
    else:
        experience_needed = next_level.experience_needed
    
    age = request.user.profile.current_pet.get_age_in_days()
    
    if not 'experience_gained' in data:
        data['experience_gained'] = -1
    if not 'levels_gained' in data:
        data['levels_gained'] = -1
        
    happiness_data = request.user.profile.current_pet.get_happiness_last_seven_days()#[25, 50, 40, 70, 10, 80, 60]#temp data
    experience_data = request.user.profile.current_pet.get_experience_last_seven_days()#[2500, 5000, 4000, 7000, 1000, 8000, 6000]
    
        
    level_data = {"current_experience": request.user.profile.current_pet.get_total_experience(), "experience_to_next_level": experience_needed, "current_level": request.user.profile.current_pet.level.level} #get_current_level()
    
    return render(request, 'tracktivityPetsWebsite/dashboard.html',  
                  {
                   "synched": fitbit_synched,
                   "happiness_graph_data": happiness_data,
                   "experience_graph_data": experience_data,
                   "mood": mood,
                   "level_data": level_data,
                   "age": age,
                   "experience_gained": data['experience_gained'],
                   "levels_gained": data['levels_gained']
                   })