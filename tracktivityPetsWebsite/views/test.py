from django.http import HttpResponse
from datetime import datetime
import hashlib, binascii
from django.conf import settings
import urllib.request #for fitbit http requests
import urllib.parse
import json

def test(request):
    
    user = request.user
    profile = user.profile
    
    #d_from.strftime('%Y-%m-%d') #todays date in format yyyy-mm-dd
    date_from = datetime.strptime("10 07 2015", "%d %m %Y").strftime('%Y-%m-%d')
        
    now = datetime.now()
    date_to = now.strftime('%Y-%m-%d') #todays date in format yyyy-mm-dd
    
    try:
        url = request.META['HTTP_HOST']
        username = user.get_username()
        hash = hashlib.pbkdf2_hmac('sha256', username.encode(), settings.SECRET_KEY.encode(), 100000)#compute secure hash so people cant intercept this crappy call (since request object doesnt work)
        params = urllib.parse.urlencode({'hash': binascii.hexlify(hash), 'username': username, 'base_date': str(date_from),  'period':'1d'})
        f = urllib.request.urlopen("http://" + url + "/fitbit/get_data/activities/steps/?" + params)#make a request to this page
        data = f.read().decode('utf-8')#whats returned 
    except Exception as e:
        return HttpResponse(str(e)) #TODO: make this something useful
    
    data_json = json.loads(data)#change it from text to something usable

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

    if data_json['meta']['status_code'] != 100:#temp stuff for testing
        return False, data_json['meta']['status_code']#TODO: make this something useful
   ''' 
    return HttpResponse(data_json['meta']['status_code'])
    
    experience = 0

    for date in data_json['objects']: #terrible code reuse
        if date['dateTime'] == date_from: #this day may already have data, if its synced multiple times a day, should do this a less exhaustive way though
            try:#update it
                existing_experience = Experience.objects.get(pet=profile.current_pet, date=str(date['dateTime']) + " 00:00:00+00:00")
                existing_happiness = Happiness.objects.get(pet=profile.current_pet, date=str(date['dateTime']) + " 00:00:00+00:00")

                happiness = max(min(int(date['value']) / 100, 100), 0) #100 is used to set '100%'
                existing_happiness.amount = happiness
                existing_experience.amount = date['value']
                experience += int(date['value']) - int(existing_experience.amount) #new - old = amount gained
                existing_experience.save()
                existing_happiness.save()
                
            except ObjectDoesNotExist: #only create a new one for it if the day doesnt exist, which should presumably only be the first ever time
                exp = Experience.objects.create(pet=profile.current_pet, amount=int(date['value']), date=date['dateTime'])
                experience += exp.amount
                happiness = max(min(int(date['value']) / 100, 100), 0) #100 is used to set '100%'
                Happiness.objects.create(pet=profile.current_pet, amount=int(happiness), date=date['dateTime'])
        else:
            exp = Experience.objects.create(pet=profile.current_pet, amount=int(date['value']), date=date['dateTime'])
            experience += exp.amount
            happiness = max(min(int(date['value']) / 100, 100), 0) #100 is used to set '100%'
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
    return HttpResponse("Test")