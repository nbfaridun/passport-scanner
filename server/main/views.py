from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import logging
from django.contrib.auth.decorators import login_required
from .forms import UserImageForm
from .extractor import passport
import json
from .models import Passport
from datetime import datetime
from django.conf import settings

import os

# Create your views here.

from django.http import HttpResponse

loggedClient = None

logger = logging.getLogger('main')

def index(request):
    global loggedClient
    context = {"error":None}

    if request.user.is_authenticated:
        return redirect("main")


    if request.method == 'POST':
        password = request.POST["password"]
        username = request.POST["username"]
        user = authenticate(request, username=username, password=password)
        

        if user:
            login(request, user)
            request.session['username'] = username
            logger.info(f"USER: {username} -> Has logged-in to the system")
            print("user!!!")
            return redirect("main")
        else:
            logger.error(f"USER: {username} -> Wrote a wrong login/password")
            context["error"] = "wrong password or login"
            print("not user!!!!!!")

    
    return render(request=request, template_name="sign-in.html",context=context)

@login_required
def content(request):
    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES)
        if form.is_valid():
            user_image = form.save()
            logger.info(f"USER: {request.session.get('username')} -> Has uploaded a passport")

            # Process the uploaded image with extractor.py
            image_path = user_image.image.path
            json_file_name = os.path.join(settings.BASE_DIR, "data.json")
            passport(image_path, json_file_name)

            # Load JSON data and save it to the database
            with open(json_file_name, 'r') as file:
                data = json.load(file)
            save_passport_data(data)

            # Remove the JSON file
            os.remove(json_file_name)

            return redirect('success')
    else:
        form = UserImageForm()
    return render(request, 'main.html', {'form': form})

def logout_view(request):
    global loggedClient
    logger.info(f"USER: {request.session.get('username')} -> Has logged out from the system")
    loggedClient = None
    logout(request)
    return redirect('index')

def datas_view(request):
    passports = Passport.objects.all()
    return render(request, 'datas.html', {'passports': passports})

def success_view(request):
    return render(request, 'success.html')

def save_passport_data(data):
    passport = Passport(
        type=data['Type'],
        issuing_country=data['Issuing_Country'],
        surname=data['Surname'],
        name=data['Name'],
        passport_number=data['Passport_Number'],
        nationality=data['Nationality'],
        dob=data['DOB'],
        sex=data['Sex'],
        doe=data['DOE'],
    )
    passport.save()
    print(passport)
