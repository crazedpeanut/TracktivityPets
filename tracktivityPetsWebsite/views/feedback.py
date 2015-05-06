from django.shortcuts import render
from django.http import HttpResponse


def feedback(request):
    return render(request, 'tracktivityPetsWebsite/feedback.html')


# <input type="text" id="formfill" class="form-submitting" placeholder="First name" required autofocus /> for html stuff