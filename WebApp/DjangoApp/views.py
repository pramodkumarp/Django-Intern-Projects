from django.shortcuts import render, redirect
from DjangoApp.models import Employee



def home(request):
    user = Employee.objects.all()
    return render(request, 'home.html', {'users':user})


def create_page(request):
    return render(request, 'createpage.html')


def create(request):
    employee = Employee(
        name = request.POST['user_name'],
        email = request.POST['user_email'],
        phone = request.POST['user_phone'],
    )
    employee.save()
    success = "Data successfully inserted"
    return  render(request,'createpage.html',{'success':success})



def details_page(request, id):
    employee = Employee.objects.get(id=id)
    return render(request, 'details_page.html', {'employee':employee})


def edit_page(request, id):
    employee = Employee.objects.get(id=id)
    return render(request, 'edit_page.html',{'employee':employee})


def update(request, id):
    employee = Employee.objects.get(id=id)
    employee.name = request.POST['user_name']
    employee.email = request.POST['user_email']
    employee.phone = request.POST['user_phone']
    employee.save()

    return redirect('/')


def delete(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()

    return redirect('/')