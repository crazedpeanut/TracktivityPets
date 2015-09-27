from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
    
def user_logout(request):
    '''
    The user_logout method kills a logged in users session so they have to log in again to use their account.
    '''
    
    if request.user.is_authenticated(): #if user is logged in
        logout(request) #log them out
        
    return HttpResponseRedirect(reverse('tracktivityPetsWebsite:user_login'))
