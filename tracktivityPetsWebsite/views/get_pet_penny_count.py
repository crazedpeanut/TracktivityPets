from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def get_pet_penny_count(request):
    return HttpResponse(request.user.profile.total_pet_pennies)