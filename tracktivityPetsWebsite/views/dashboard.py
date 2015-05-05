from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
import fitapp
from tracktivityPetsWebsite import utils

@login_required
def dashboard(request):
    fitbit_synched = False;
    if fitapp.utils.is_integrated(request.user):
        fitbit_synched = True
        
    start_url = static('tracktivityPetsWebsite/images')
    happiness_data = [25, 50, 40, 70, 10, 80, 60]#temp data
    experience_data = [2500, 5000, 4000, 7000, 1000, 8000, 6000]
    mood = {"phrase": "I'm so happy", "image": '{url}/pets/{name}/{location}" />'.format(url=start_url, name='Melvin', location='happyface.png')}
    level_data = {"experience": 100, "experioence_to_next_level": 200, "current_level": 5}
    age = 20
    data = utils.update_user_fitbit(request)
    
    if not 'experience_gained' in data:
        data['experience_gained'] = -1
    if not 'levels_gained' in data:
        data['levels_gained'] = -1
    
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