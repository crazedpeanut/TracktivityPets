from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required

@login_required
def feedback(request):
    '''
	The feedback method renders the feedback template and returns it to the user.
	If the type of the request is POST then an email will be sent to the development team
	with comments from the user.
	'''
	
    if request.method == "POST":
        contents = request.POST.get("contents", None)
        
        if contents is None or contents is "":
            return render(request, 'tracktivityPetsWebsite/feedback.html')
        
        username = request.user.get_username()

        user_email = 'john@johnkendall.net'
        email_to = "pets@bitlink.com.au"
        subject = "Tracktivity Pets Feedback from " + username
        
        try:
            send_mail(subject, contents, user_email, [email_to], fail_silently=False)
        except BadHeaderError as e:
            return render(request, 'tracktivityPetsWebsite/feedback.html', {'error':'Bad header'})
            
        return render(request, 'tracktivityPetsWebsite/feedback.html', {'success':'Message sent successfully'})
    return render(request, 'tracktivityPetsWebsite/feedback.html')