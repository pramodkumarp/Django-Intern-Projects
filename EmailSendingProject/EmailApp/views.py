from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings


def email(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        from_email  =settings.EMAIL_HOST_USER
        rcvr = [request.POST['toemail'],]

        send_mail(subject, message, from_email, rcvr)
        request.session['success'] = 'Email successfully sent to {}'.format(rcvr[0])

        return redirect('/success/')
    else:
        return render(request, 'index.html')


def success(request):
    return render(request, 'success.html')
