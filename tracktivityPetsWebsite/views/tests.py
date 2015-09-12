__author__ = 'John'

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from tracktivityPetsWebsite.tasks import check_user_challenges

def test_challenge_check(request):
    check_user_challenges.delay(request.user)
    return HttpResponse("All Done")