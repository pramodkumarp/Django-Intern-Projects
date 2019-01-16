from django.shortcuts import render, redirect
from .models import Employee
from django.utils.datastructures import MultiValueDictKeyError
import os
from datetime import datetime



def home(request):
    employee = Employee.objects.all()
    return render(request, "backEnd/homeContent/homeContent.html", {"employee":employee})


def create_new_user(request):
    return  render(request, "backEnd/createNewUser/createNewUser.html")


def add_user(request):
    employee = Employee()

    try:
        employee.user_name= request.POST["user_name"]
        employee.user_email= request.POST["user_email"]
        employee.user_phone= request.POST["user_phone"]
        employee.user_country= request.POST["user_country"]
        employee.user_city= request.POST["user_city"]
        employee.user_state= request.POST["user_state"]
        employee.user_zip= request.POST["user_zip"]
        employee.user_gender= request.POST['user_gender']
        employee.user_about= request.POST["user_about"]
        employee.user_image= request.FILES["user_image"]
        employee.user_creation_date= datetime.now().date()
        employee.save()

        return redirect("/")

    except MultiValueDictKeyError:
        employee.user_name = request.POST["user_name"]
        employee.user_email = request.POST["user_email"]
        employee.user_phone = request.POST["user_phone"]
        employee.user_country = request.POST["user_country"]
        employee.user_city = request.POST["user_city"]
        employee.user_state = request.POST["user_state"]
        employee.user_zip = request.POST["user_zip"]
        employee.user_gender = request.POST['user_gender']
        employee.user_about = request.POST["user_about"]
        employee.user_creation_date = datetime.now().date()
        employee.save()

        return redirect("/")


def edit_user(request, id):
    employee = Employee.objects.get(id=id)
    return render(request, "backEnd/editUserData/edit_user_data.html",{"employee":employee})

def edit(request, id):
    employee = Employee.objects.get(id=id)
    try:
        employee.user_name = request.POST["user_name"]
        employee.user_email = request.POST["user_email"]
        employee.user_phone = request.POST["user_phone"]
        employee.user_country = request.POST["user_country"]
        employee.user_city = request.POST["user_city"]
        employee.user_state = request.POST["user_state"]
        employee.user_zip = request.POST["user_zip"]
        employee.user_gender = request.POST['user_gender']
        employee.user_about = request.POST["user_about"]
        employee.user_image = request.FILES["user_image"]
        employee.user_creation_date = datetime.now().date()

        employee.save()
        return redirect("/")

    except MultiValueDictKeyError:
        employee.user_name = request.POST["user_name"]
        employee.user_email = request.POST["user_email"]
        employee.user_phone = request.POST["user_phone"]
        employee.user_city = request.POST["user_city"]
        employee.user_state = request.POST["user_state"]
        employee.user_zip = request.POST["user_zip"]
        employee.user_about = request.POST["user_about"]
        employee.user_info_last_update = datetime.now().date()

        employee.save()
        return redirect("/")




def user_details(request, id):
    employee = Employee.objects.get(id=id)
    return render(request, "backEnd/userDetails/userDetails.html", {"employee":employee})


def delete(request, id):
    employee = Employee.objects.get(id=id)
    try:
        path = employee.user_image.path
        if os.path.isfile(path):
            os.remove(path)
        employee.delete()

        return redirect("/")
    except ValueError:
        employee.delete()
        return redirect("/")