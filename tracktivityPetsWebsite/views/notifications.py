from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from tracktivityPetsWebsite.models import MicroChallenge, MicroChallengeGoal, MicroChallengeMedal, \
    UserMicroChallenge, UserMicroChallengeState, MicroChallengeState, UserMicroChallengeGoalStatus,\
    UserNotification

from django.core import serializers
import datetime

def get_unacknowledged_notifications(request):
    '''
    The get_unacknowledged_notifications returns all of the UserNotification instances 
    that haven't been acknowledged and return them in JSON format.
    '''

    notifications = UserNotification.objects.filter(userProfile=request.user.profile, acknowledged=False)
    return HttpResponse((serializers.serialize("json", notifications)), content_type="application/json")

def acknowledge_notification(request, notification_pk):
    '''
    Set a UserNotification instances acknowledged property to True.
    '''
	
    notification = UserNotification.objects.filter(pk=notification_pk)
    notification.acknowledged = True
    notification.save()

