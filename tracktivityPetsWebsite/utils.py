import fitapp

def update_user_fitbit(user):
    #pull steps from last_fitbit_sync upto today
    #run through each one and add new steps
    #last_fitbit_sync may already contain data for that day, but different, need to do new - old and add to that day
    #add to current pet experience and happiness
    #save it all
    #return True if succeed, False if something went wrong
    pass

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

def is_fitbit_linked(user):
    return fitapp.utils.is_integrated(user)
