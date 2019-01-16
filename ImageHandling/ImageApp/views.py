from django.shortcuts import render, redirect
from .models import ImageHandling
from django.utils.datastructures import MultiValueDictKeyError
import os




def index(request):
    img = ImageHandling.objects.all()
    return render(request, 'index.html',{'img':img})


def upload(request):
    img = ImageHandling(
        name= request.POST['name'],
        image=request.FILES['image']
    )
    img.save()

    return redirect('/')


def edit(request, id):
    img = ImageHandling.objects.get(id=id)
    return render(request, 'edit.html', {'img':img})


def update(request, id):
    img = ImageHandling.objects.get(id=id)
    try:
        img.name = request.POST['name']
        img.image = request.FILES['image']
        img.save()
        return  redirect('/')
    except MultiValueDictKeyError:
        img.name = request.POST['name']
        img.save()
        return  redirect('/')


def delete(request, id):
    img = ImageHandling.objects.get(id=id)
    path = img.image.path
    if os.path.isfile(path):
        os.remove(path)
    img.delete()

    return redirect('/')

