import fitapp
from django.contrib.auth.models import User
from tracktivityPetsWebsite.models import Inventory, Profile, CollectedPet, Level, Pet
import datetime
import urllib.request #for fitbit http requests
import urllib.parse
import django
from django.core.urlresolvers import reverse
import fitapp
from django.contrib.sites.models import get_current_site
import datetime

''' gets the steps from last_fitbit_sync to today, handles and stores the data in happiness/experience models '''
def update_user_fitbit(request):
    if not is_fitbit_linked(request.user):
        return False

    #pull steps from last_fitbit_sync upto today
    if request.user.profile.last_fitbit_sync is None:
        date_from = request.user.date_joined #need to format this from a datetime
    else:
        date_from = request.user.profile.last_fitbit_sync
        
    now = datetime.datetime.now()
    date_to = t.strftime('%Y-%m-%d') #todays date in format yyyy-mm-dd
    
    print(date_to)
    
    try:
        #TODO: MAJOR SECURITY RISK - hash username or some crap to make it more secure
        url = request.META['HTTP_HOST']
        params = urllib.parse.urlencode({'username': request.user.get_username(),'base_date': date_from, 'end_date': date_to})
        f = urllib.request.urlopen("http://" + url + "/fitbit/get_data/activities/steps/?" + params)
        data = f.read().decode('utf-8')
    except Exception as e:
        return str(e)
    
    #TODO: need to compensate for all the possible codes recieved from fitbit-django (such as 101, etc)
    
    #change last_fitbit_sync to todays date
    
    #run through each one and add new steps
        #last_fitbit_sync may already contain data for that day, but different, need to do new - old and add to that day
        #add to current pet experience and happiness
        #save it all (each new happiness and experience in the for loop)
    #return True if succeed, False if something went wrong

''' A new user is created based up values passed in, returns None if there is no problems, otherwise a string with the error '''
#TODO: untested
def register_user(first_name, last_name, email, username, password, confirm_password):
    if password != confirm_password or password == '' or email == '' or username == '':
        return 'Not all values have been set'
    
    try:
        user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        inventory = Inventory.objects.create()
        inventory.save()
        profile = Profile.objects.create(user=user, inventory=inventory)
        profile.save()
        user.save()
        return None
    except Exception as e:
        return str(e)
    
    return None

''' Used for when a user picks their first pet. Creates a new current pet and assigns it to the user '''
#TODO: Untested
def register_pet_selection(user, pet, name):
    try: #gross code, if it passes this then they have a pet, otherwise it throws an exception and we make a new pet
        user.profile.current_pet
        return False
    except:
        try:
            level = Level.objects.get(level=1) #dodgy code, but can presume level 1 will always exist
            now = datetime.datetime.now()
            profile = Profile.objects.get(user=user) #should change this to form of user.profile, but it doesnt seem to work 
            collected_pet = CollectedPet.objects.create(pet=pet, inventory=profile.inventory, level=level, name=name, date_created=now) #create new collected pet
            collected_pet.save()
            profile.current_pet = collected_pet #link it to user.profile.current_pet 
            profile.save()
            return True
        except Exception as e:
            return str(e)

def set_current_pet(user):
    pass

def get_happiness_graph_data(user):
    #possibly user.current_pet.happiness_set.filter(date__gt=<date 6 days ago?>)
    pass

def get_experience_graph_data(user):
    #possibly user.current_pet.experience_set.filter(date__gt=<date 6 days ago?>)
    pass

def get_current_pet_level(user):
    #possibly user.current_pet.level.level
    pass

def get_current_pet_mood(user):
    pass

def get_current_pet_phrase(user):
    #possibly same as mood, but .text at end
    pass

def get_user(request):
    return request.user

''' Returns whether a user has a linked fitbit account or not '''
def is_fitbit_linked(user):
    return fitapp.utils.is_integrated(user)
