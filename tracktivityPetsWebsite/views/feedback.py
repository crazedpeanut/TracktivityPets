from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required 

@login_required
def feedback(request):
    
    if request.method == "POST":
        contents = request.POST.get("contents", None)
        
        if contents is None or contents is "":
            return render(request, 'tracktivityPetsWebsite/feedback.html')
        
        username = request.user.get_username()
        user_email = request.user.email
        email_to = "g3325629@trbvm.com"
        subject = "Tracktivity Pets Feedback from " + username
        
        send_mail(subject, contents, user_email, [email_to], fail_silently=False)
        return HttpResponse("submitted successfully")
    return render(request, 'tracktivityPetsWebsite/feedback.html')


# <input type="text" id="formfill" class="form-submitting" placeholder="First name" required autofocus /> for html stuff