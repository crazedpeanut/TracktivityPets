from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def get_pet_penny_count(request):
    '''
    get_pet_penny_count returns the amount of pet pennies for logged in
    user.
    '''
	
    return HttpResponse(request.user.profile.total_pet_pennies)
