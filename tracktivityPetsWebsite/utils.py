import fitapp
from django.contrib.auth.models import User
from tracktivityPetsWebsite.models import Inventory, Profile, CollectedPet, Level, Pet, Experience, Happiness
import datetime
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


''' gets the steps from last_fitbit_sync to today, handles and stores the data in happiness/experience models 
#TODO: change this to be ajax suitable, so a button press can asynchronously call this method, and then get notified that update is done
this method will probably take 2-3 seconds to run, since fitbit API can take a while to respond, so ajax would be good
means it should go in the update_user_fitbit
'''
def update_user_fitbit(request):
    if not is_fitbit_linked(request.user) or request.user.profile.current_pet is None:
        return False
    
    user = request.user
    profile = user.profile
    
    #pull steps from last_fitbit_sync upto today
    if profile.last_fitbit_sync is None:
        d_from = user.date_joined
    else:
        d_from = profile.last_fitbit_sync
        
    date_from = d_from.strftime('%Y-%m-%d') #todays date in format yyyy-mm-dd
        
    now = datetime.datetime.now()
    date_to = now.strftime('%Y-%m-%d') #todays date in format yyyy-mm-dd
    
    try:
        url = request.META['HTTP_HOST']
        username = user.get_username()
        hash = hashlib.pbkdf2_hmac('sha256', username.encode(), settings.SECRET_KEY.encode(), 100000)#compute secure hash so people cant intercept this crappy call (since request object doesnt work)
        params = urllib.parse.urlencode({'hash': binascii.hexlify(hash), 'username': username, 'base_date': str(date_from), 'end_date': str(date_to)})
        f = urllib.request.urlopen("http://" + url + "/fitbit/get_data/activities/steps/?" + params)#make a request to this page
        data = f.read().decode('utf-8')#whats returned 
    except Exception as e:
        return str(e) #TODO: make this something useful
    
    data_json = json.loads(data)#change it from text to something usable
    
    #TODO: need to compensate for all the possible codes recieved from fitbit-django (such as 101, etc)
    if data_json['meta']['status_code'] != 100:#temp stuff for testing
        data_to_return = {}
        data_to_return['experience_gained'] = data_json
        data_to_return['levels_gained'] = -1
        return data_to_return
    
    experience = 0

    for date in data_json['objects']: #terrible code reuse
        if date['dateTime'] == date_from: #this day may already have data, if its synced multiple times a day, should do this a less exhaustive way though
            try:#update it
                existing_experience = Experience.objects.get(pet=profile.current_pet, date=str(date['dateTime']) + " 00:00:00+00:00")
                existing_happiness = Happiness.objects.get(pet=profile.current_pet, date=str(date['dateTime']) + " 00:00:00+00:00")

                happiness = max(min(int(date['value']) / 75, 100), 0) #75 is used to set '100%'
                existing_happiness.amount = happiness
                existing_experience.amount = date['value']
                experience += int(date['value']) - int(existing_experience.amount) #new - old = amount gained
                existing_experience.save()
                existing_happiness.save()
                
            except ObjectDoesNotExist: #only create a new one for it if the day doesnt exist, which should presumably only be the first ever time
                exp = Experience.objects.create(pet=profile.current_pet, amount=int(date['value']), date=date['dateTime'])
                experience += exp.amount
                happiness = max(min(int(date['value']) / 75, 100), 0) #75 is used to set '100%'
                Happiness.objects.create(pet=profile.current_pet, amount=int(happiness), date=date['dateTime'])
        else:
            exp = Experience.objects.create(pet=profile.current_pet, amount=int(date['value']), date=date['dateTime'])
            experience += exp.amount
            happiness = max(min(int(date['value']) / 75, 100), 0) #75 is used to set '100%'
            Happiness.objects.create(pet=profile.current_pet, amount=int(happiness), date=date['dateTime'])
            
    current_level = profile.current_pet.level.level
    update_pet_level(profile.current_pet)
    new_level = profile.current_pet.level.level

    data_to_return = {}
    data_to_return['experience_gained'] = experience
    data_to_return['levels_gained'] = new_level - current_level #TODO
    #data_to_return['pet_pennies_gained'] = 0
    
    #happiness += int(date['value']) / data_json['meta']['total_count'] / 75 #need to cap this at 100 #if ever want average of the retrieved stuff
    
    #change last_fitbit_sync to todays date
    profile.last_fitbit_sync = date_to
    profile.save()
    
    return data_to_return
    #if request.method == GET
        #return ajax friendly data
    #else
        #render dashboard page

''' A new user is created based up values passed in, returns None if there is no problems, otherwise a string with the error '''
#TODO: untested
def register_user(first_name=None, last_name=None, email=None, username=None, password=None, confirm_password=None, registerForm=None):
    if(registerForm == None): #Chosen to input fields manually
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
    elif(registerForm.is_valid()): #Using registerForm to enter details
            username = registerForm.cleaned_data['username']
            password = registerForm.cleaned_data['password']
            confirmPass = registerForm.cleaned_data['confirmPass']
            firstName = registerForm.cleaned_data['firstname']
            surname = registerForm.cleaned_data['surname']
            email = registerForm.cleaned_data['email']
            
            if password != confirmPass or password == '' or email == '' or email == '':
                return 'Not all values have been set'
            
            try:
                user = User.objects.create_user(username, email, password, first_name=firstname.firstname, last_name = surname)
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


def set_current_pet(user):
    pass


def get_user(request):
    return request.user

''' Returns whether a user has a linked fitbit account or not '''
def is_fitbit_linked(user):
    return fitapp.utils.is_integrated(user)
