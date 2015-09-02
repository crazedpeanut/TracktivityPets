from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from tracktivityPetsWebsite.models import MicroChallenge, MicroChallengeGoal, MicroChallengeMedal,\
    UserMicroChallenge, UserMicroChallengeState, MicroChallengeState
from django.core import serializers
import datetime

import json

@login_required
def challenges(request):
    return render(request, 'tracktivityPetsWebsite/challenges/challenges.html')

@login_required
def get_available_challenge_names(request):
    challenges = list(MicroChallenge.objects.all())
    current_challenges = UserMicroChallenge.objects.filter(profile=request.user.profile)

    for c in challenges:
        for cc in current_challenges:
            if c == cc.micro_challenge:
                challenges.remove(c)

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

@login_required
def get_active_challenge_details(request, user_challenge_pk):
    uc = UserMicroChallenge.objects.get(pk=user_challenge_pk)

    challenge = uc.micro_challenge

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
        'goals':goals_list,
        'max_steps':uc.state.state.steps
    }

    response_json = json.dumps(response)

    return HttpResponse( response_json, content_type="application/json")

@login_required
def get_complete_challenge_details(request, user_challenge_pk):
    uc = UserMicroChallenge.objects.get(pk=user_challenge_pk)

    challenge = uc.micro_challenge

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
        'goals':goals_list,
        'max_steps':uc.state.state.steps
    }

    response_json = json.dumps(response)

    return HttpResponse(response_json, content_type="application/json")

@login_required
def get_active_challenge_names(request):
    user_challenges = UserMicroChallenge.objects.filter(profile=request.user.profile, complete=False)
    challenge_names = []

    for uc in user_challenges:
        challenge_names.append({'pk':uc.pk, 'name':uc.micro_challenge.name})

    return HttpResponse(json.dumps(challenge_names), content_type="json/application")

@login_required
def get_completed_challenge_names(request):
    user_challenges = UserMicroChallenge.objects.filter(profile=request.user.profile, complete=True)
    challenge_names = []

    for uc in user_challenges:
        challenge_names.append({'pk':uc.pk, 'name':uc.micro_challenge.name})

    return HttpResponse(json.dumps(challenge_names), content_type="json/application")

@login_required
def accept_challenge(request, challenge_pk):
    micro_chal = MicroChallenge(pk=challenge_pk)
    chal_state = MicroChallengeState(steps=0)
    user_chal_state = UserMicroChallengeState(state=chal_state)

    date_end = datetime.datetime.now() + datetime.timedelta(minutes=micro_chal.duration_mins)

    user_chal = UserMicroChallenge(state=user_chal_state, micro_challenge=challenge_pk,profile=request.user.profile, date_end=date_end)

    chal_state.save()
    user_chal_state.save()
    user_chal.save()