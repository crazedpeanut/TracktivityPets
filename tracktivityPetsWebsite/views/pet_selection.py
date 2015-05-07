from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

@login_required
def pet_selection(request):
    return HttpResponse('TODO: pet selection page')