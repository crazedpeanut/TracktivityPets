import fitapp
import logging
from django.contrib.auth.models import User
from tracktivityPetsWebsite.models import Inventory, Profile, CollectedPet, Level, Pet
from tracktivityPetsWebsite.models import Experience, Happiness, Story, Item, CollectedItem, PetSwap
import urllib.request #for fitbit http requests
import urllib.parse
import django
from django.core.urlresolvers import reverse
import fitapp
from django.contrib.sites.models import get_current_site
import datetime
import hashlib
from django.conf import settings
import hashlib, binascii
import json
from django.core.exceptions import ObjectDoesNotExist
from django.templatetags.static import static

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
hdlr = logging.FileHandler(settings.BASE_DIR + 'tracktivitypets_utils.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


#TODO: need to compensate for all the possible codes recieved from fitbit-django (such as 101, etc)
'''
 When everything goes well, the *status_code* is 100 and the requested data
is included. However, there are a number of things that can 'go wrong'
with this call. For each type of error, we return an empty data list with
a *status_code* to describe what went wrong on our end:

    :100: OK - Response contains JSON data.
    :101: User is not logged in.
    :102: User is not integrated with Fitbit.
    :103: Fitbit authentication credentials are invalid and have been
        removed.
    :104: Invalid input parameters. Either *period* or *end_date*, but not
        both, must be supplied. *period* should be one of [1d, 7d, 30d,
        1w, 1m, 3m, 6m, 1y, max], and dates should be of the format
        'yyyy-mm-dd'.
    :105: User exceeded the Fitbit limit of 150 calls/hour.
    :106: Fitbit error - please try again soon.
'''
def retrieve_fitapp_data(user, d_from, date_to):
    if not is_fitbit_linked(user):
        return False, 'No fitbit found'
    elif user.profile.current_pet is None:
        return False, 'No current pet'

    try:
        url = settings.HOST_NAME
        username = user.get_username()
        #compute secure hash so people cant intercept this crappy call (since request object doesnt work)
        hash = hashlib.pbkdf2_hmac('sha256', username.encode(), settings.SECRET_KEY.encode(), 100000)
        params = urllib.parse.urlencode({'hash': binascii.hexlify(hash),
                                         'username': username,
                                         'base_date': str(d_from),
                                         'end_date': str(date_to)})
        #make a request to this page
        f = urllib.request.urlopen("http://" + url + "/fitbit/get_data/activities/steps/?" + params)
        data = f.read().decode('utf-8')#whats returned
    except Exception as e:
        logger.debug(str(e))
        return False, str(e) #TODO: make this something useful

    logger.debug(data)

    return True, json.loads(data)#change it from text to something usable

''' gets the steps from last_fitbit_sync to today, handles and stores the data in happiness/experience models 
#TODO: change this to be ajax suitable, so a button press can asynchronously call this method, and then get notified that update is done
this method will probably take 2-3 seconds to run, since fitbit API can take a while to respond, so ajax would be good
means it should go in the update_user_fitbit
'''
#TODO: Gets all steps for the day, and doesnt consider other pets already having steps for it
#Not going to effect release 1, but needs to change for release 2. Will have to loop through each pet in users inventory, get the experience for the day, add it all up, minus that from the total steps, and then add that to the pet
def update_user_fitbit(request):

    profile = request.user.profile

    #pull steps from last_fitbit_sync upto today
    if profile.last_fitbit_sync is None:
        d_from = request.user.date_joined
    else:
        d_from = profile.last_fitbit_sync

    date_from = d_from.strftime('%Y-%m-%d') #todays date in format yyyy-mm-dd

    now = datetime.datetime.now()
    date_to = now.strftime('%Y-%m-%d') #todays date in format yyyy-mm-dd

    result, data = retrieve_fitapp_data(request.user, d_from, date_to)

    if(result is False):
        logger.debug(data)

    data_json = data

    if data_json['meta']['status_code'] != 100:#temp stuff for testing
        return False, data_json['meta']['status_code']#TODO: make this something useful

    experience = 0

    for date in data_json['objects']: #terrible code reuse

        datetime_object = datetime.strptime(date['dateTime'])
        swap_counts = count_pet_swaps_for_day(datetime_object)
        swap_counts += 1

        if date['dateTime'] == date_from: #this day may already have data, if its synced multiple times a day, should do this a less exhaustive way though
            try:#update it
                existing_experience = Experience.objects.get(pet=profile.current_pet, date=str(date['dateTime']) + " 00:00:00+00:00")
                existing_happiness = Happiness.objects.get(pet=profile.current_pet, date=str(date['dateTime']) + " 00:00:00+00:00")

                happiness = max(min(int(date['value']) / 100, 100), 0) #100 is used to set '100%'
                happiness / swap_counts #Division of happiness and experience for pets active throughout day
                existing_happiness.amount = happiness
                existing_experience.amount = date['value'] / swap_counts #Division of happiness and experience for pets active throughout day
                experience += int(date['value']) - int(existing_experience.amount) #new - old = amount gained
                existing_experience.save()
                existing_happiness.save()
                
            except ObjectDoesNotExist: #only create a new one for it if the day doesnt exist, which should presumably only be the first ever time
                exp = Experience.objects.create(pet=profile.current_pet, amount=int(date['value']), date=date['dateTime'])
                experience += exp.amount
                happiness = max(min(int(date['value']) / 100, 100), 0) #100 is used to set '100%'
                happiness / swap_counts #Division of happiness and experience for pets active throughout day
                Happiness.objects.create(pet=profile.current_pet, amount=int(happiness), date=date['dateTime'])
        else:
            exp = Experience.objects.create(pet=profile.current_pet, amount=int(date['value']), date=date['dateTime'])
            experience += exp.amount
            happiness = max(min(int(date['value']) / 100, 100), 0) #100 is used to set '100%'
            happiness / swap_counts #Division of happiness and experience for pets active throughout day
            Happiness.objects.create(pet=profile.current_pet, amount=int(happiness), date=date['dateTime'])
            
    current_level = profile.current_pet.level.level
    update_pet_level(profile.current_pet)
    new_level = profile.current_pet.level.level           

    data_to_return = {}
    data_to_return['experience_gained'] = experience
    data_to_return['levels_gained'] = new_level - current_level #TODO
    #data_to_return['pet_pennies_gained'] = 0
    data_to_return['stories'] = {}
    
    #see if any new stories are unlocked and create UserStory here
    level = current_level + 1
    combined = ''
    while level <= new_level:
        try:
            l = Level.objects.get(level=level)
            story = Story.objects.get(level_unlocked=l, pet=profile.current_pet.pet)#get any stories for that level
            data_to_return['stories'][l.level] = story
        except:
            pass #no story for this level
        level += 1
    
    #happiness += int(date['value']) / data_json['meta']['total_count'] / 100 #need to cap this at 100 #if ever want average of the retrieved stuff
    
    #change last_fitbit_sync to todays date
    profile.last_fitbit_sync = date_to
    profile.save()
    
    return True, data_to_return
    #if request.method == GET
        #return ajax friendly data
    #else
        #render dashboard page

def count_pet_swaps_for_day(day):
    swaps = PetSwap.objects.filter(time_swapped__year=day.date.year, time_swapped__day=day.date.day, time_swapped__month=day.date.month)
    return swaps.count()

''' A new user is created based up values passed in, returns None if there is no problems, otherwise a string with the error '''
def register_user(first_name=None, last_name=None, email=None, username=None, password=None, confirm_password=None, registerForm=None):
    if registerForm is not None and registerForm.is_valid(): #Using registerForm to enter details
            username = registerForm.cleaned_data['username'].lower()
            password = registerForm.cleaned_data['password']
            confirmPass = registerForm.cleaned_data['confirmPass']
            firstName = registerForm.cleaned_data['firstname'].lower()
            surname = registerForm.cleaned_data['surname'].lower()
            email = registerForm.cleaned_data['email'].lower()
            
            if password != confirmPass or password == '' or email == '' or email == '':
                return 'Not all values have been set'
            
            try:
                user = User.objects.create_user(username.lower(), email.lower(), password.lower(), first_name=firstName.lower(), last_name = surname.lower())
                inventory = Inventory.objects.create()
                inventory.save()
                profile = Profile.objects.create(user=user, inventory=inventory)
                profile.save()
                user.save()
                return None
            except Exception as e:
                return str(e)
            
        

''' Used for when a user picks their first pet. Creates a new current pet and assigns it to the user '''
#TODO: Untested
def register_pet_selection(user, pet, name):
    if user.profile.current_pet is not None:
        return False, None #user already has a current pet
    else:
        try:
            level = Level.objects.get(level=1) #dodgy code, but can presume level 1 will always exist
            now = datetime.datetime.now()
            profile = Profile.objects.get(user=user) #should change this to form of user.profile, but it doesnt seem to work 
            collected_pet = CollectedPet.objects.create(pet=pet, inventory=profile.inventory, level=level, name=name, date_created=now) #create new collected pet
            collected_pet.save()
            profile.current_pet = collected_pet #link it to user.profile.current_pet 
            profile.save()
            return True, None
        except Exception as e:
            return False, str(e)

#forces a refresh on the pet to see if it's level should be different
def update_pet_level(collected_pet):
    try:
        experience = collected_pet.get_total_experience()
        level = Level.objects.filter(experience_needed__lte=experience).order_by('-experience_needed')
        collected_pet.level = level[0]
        collected_pet.save()
        return True
    except:
        return False
            
def update_pet_level_with_value(collected_pet, experience):
    try:
        level = Level.objects.filter(experience_needed__lte=experience).order_by('-experience_needed')
        collected_pet.level = level[0]
        collected_pet.save()
        return True
    except:
        return False

def get_pet_selection_data():
    pets = Pet.objects.all()
    levelOne = Level.objects.get(level=1)
    data = {}
    start_url = static('tracktivityPetsWebsite/images')
    
    for pet in pets:
        try:
            data[pet.default_name] = {}
            data[pet.default_name]['name'] = pet.default_name
            data[pet.default_name]['story'] = pet.story_set.filter(level_unlocked=levelOne)[0].text#get the level one story for each pet
            image_location = pet.mood_set.filter(happiness_needed=-1)[0].image_location
            data[pet.default_name]['image'] = '{url}/pets/{name}/{location}'.format(url=start_url, name=pet.default_name, location=image_location)
            silohuette_image_location = pet.mood_set.filter(happiness_needed=-2)[0].image_location
            data[pet.default_name]['silohuette'] = '{url}/pets/{name}/{location}'.format(url=start_url, name=pet.default_name, location=silohuette_image_location)
        except:
            pass #do nothing, but pet isnt set up properly in admin view (needs a story at level 1, and image at -1 happiness)
    return data

def get_current_pet(user):
    return user.profile.current_pet

def set_current_pet(user, owned_pet):
    try:
        num_pets = CollectedPet.objects.filter(inventory=user.profile.inventory)
        if(num_pets.count > 0):
            pet_swap = PetSwap(from_pet=user.profile.current_pet, to_pet=owned_pet)
            user.profile.current_pet = owned_pet
            user.profile.save()
            return True
    except:
        return False

def get_user(request):
    return request.user

''' Returns whether a user has a linked fitbit account or not '''
def is_fitbit_linked(user):
    return fitapp.utils.is_integrated(user)

def generate_pet_image_url(pet, image_location):
    start_url = static('tracktivityPetsWebsite/images')
    return '{url}/pets/{name}/{location}'.format(url=start_url, name=pet.default_name, location=image_location)















