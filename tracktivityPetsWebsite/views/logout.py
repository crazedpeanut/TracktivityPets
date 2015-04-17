from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
    
def user_logout(request):
    if request.method == 'POST' and request.user.is_authenticated(): #if user is logged in
        logout(request) #log them out
        return HttpResponse("Logged out")
    else:
        return HttpResponse("No user to logout")
        
