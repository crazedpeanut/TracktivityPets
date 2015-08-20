from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from tracktivityPetsWebsite.models import MicroChallenge
from django.core import serializers

@login_required
def challenges(request):
    return render(request, 'tracktivityPetsWebsite/challenges/challenges.html')

@login_required
def get_available_challenge_names(request):
    challenges = MicroChallenge.objects.all()
    return HttpResponse((serializers.serialize("json", challenges)), content_type="application/json")

@login_required
def get_challenge_details(request, challenge_pk):
    challenge = MicroChallenge.objects.filter(name=challenge_pk)
    return HttpResponse((serializers.serialize("json", challenge)), content_type="application/json")

def get_active_challenge_names(request):
    HttpResponse('none')
def get_active_challenge_names(request):
    HttpResponse('none')