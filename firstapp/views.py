from . import TeleFunctions, SecretKeys
import asyncio
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth  import authenticate,  login, logout
import django.contrib.auth





api_id = 26537899
api_hash = '809d4d7586d0e8b681cbcee8d40ae568'
phone_number = "+917407609633"
group_participants = ['Cat', 'Cloudbot']


# Create your views here.

def home(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'account/signup.html')

def login(request):
    return render(request, 'account/login.html')

def handle_signup(request):
    if request.method=="POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
                
        # check for errorneous input
        # if len(username)<10:
        #     messages.error(request, " Your user name must be under 10 characters")
        #     return redirect('Home')

        # if not username.isalnum():
        #     messages.error(request, " User name should only contain letters and numbers")
        #     return redirect('home')
        # if (pass1!= pass2):
        #      messages.error(request, " Passwords do not match")
        #      return redirect('home')
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        # Create the user
        myuser = User.objects.create_user(username, email, password1)
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")

        # Telegram codes
        group_title = email
        group_id = TeleFunctions.create_telegram_group(phone_number, group_title, group_participants)
        print('group created')


        return redirect('Home')

    else:
        return HttpResponse("404 - Not found")

def handle_login(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            django.contrib.auth.login(request, user)
            messages.success(request, "Successfully Logged In")
            print('successfully logged in')
            return redirect("Home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            print('Invalid credentials! Please')
            return redirect("Home")

    return HttpResponse("404- Not found")

def handle_logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('Home')
