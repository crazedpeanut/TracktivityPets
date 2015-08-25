from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from tracktivityPetsWebsite.models import MicroChallenge, MicroChallengeGoal, MicroChallengeMedal
from django.core import serializers

import json

@login_required
def challenges(request):
    return render(request, 'tracktivityPetsWebsite/challenges/challenges.html')

@login_required
def get_available_challenge_names(request):
    challenges = MicroChallenge.objects.all()
    return HttpResponse((serializers.serialize("json", challenges)), content_type="application/json")

@login_required
def get_challenge_details(request, challenge_pk):
    challenge = MicroChallenge.objects.get(pk=challenge_pk)

    challenge_response = {
        'name':challenge.name,
        'overview':challenge.overview,
    }

    goals_list = []
    goals = list(MicroChallengeGoal.objects.filter(micro_challenge=challenge))

    for g in goals:
        goals_list.append({
            'description':g.description,
            'pet_pennies':g.pet_pennies_reward,
            'medal':g.medal.name
        })

    response = {
        'challenge':challenge_response,
        'goals':goals_list
    }

    response_json = json.dumps(response)

    return HttpResponse( response_json, content_type="application/json")

def get_active_challenge_names(request):
    HttpResponse('none')
def get_active_challenge_names(request):
    HttpResponse('none')