from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

@login_required
def store(request):
    return render(request, 'tracktivityPetsWebsite/store/store.html')