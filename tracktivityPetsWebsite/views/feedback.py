from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError


def feedback(request):
    
    if request.method == "POST":
        contents = request.POST.get("contents", None)
        
        if contents is None or contents is "":
            return render(request, 'tracktivityPetsWebsite/feedback.html')
        
        username = request.user.get_username()
        #user_email = request.user.email
        user_email = 'john@johnkendall.net' #Just for test purposes
        email_to = "pets@bitlink.com.au"
        subject = "Tracktivity Pets Feedback from " + username
        
        try:
            send_mail(subject, contents, user_email, [email_to], fail_silently=False)
        except BadHeaderError as e:
            return render(request, 'tracktivityPetsWebsite/feedback.html', {'error':'Bad header'})
            
        return render(request, 'tracktivityPetsWebsite/feedback.html', {'success':'Message sent successfully'})
    return render(request, 'tracktivityPetsWebsite/feedback.html')


# <input type="text" id="formfill" class="form-submitting" placeholder="First name" required autofocus /> for html stuff