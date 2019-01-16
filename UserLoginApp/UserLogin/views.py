from django.shortcuts import render, redirect
from .models import User


def index(request):
    if request.method == 'POST':
        user = User()
        user.user_name = request.POST['name']
        user.user_email = request.POST['email']
        user.user_pass = request.POST['password']
        user.save()
        message = "Registered successfully!"
        return render(request, 'index.html', {'message':message})
    else:
        return render(request, 'index.html')


def loging(request):

    if request.method == 'POST':
        try:
            m = User.objects.get(user_email=request.POST['email'], user_pass=request.POST['password'])
            if m.user_email == request.POST['email'] and m.user_pass == request.POST['password']:
                request.session['id'] = m.id
                request.session['name'] = m.user_name
                return redirect('/user/logged-in/dashboard/')
            else:
                message = 'User name and password invalid!'
                return render(request, 'login.html', {'message':message})
        except User.DoesNotExist:
            message = 'User name and password invalid!'
            return render(request, 'login.html', {'message': message})

    else:
        return render(request, 'login.html')


def dashboard(request):
    return render(request, 'dashboard.html')
