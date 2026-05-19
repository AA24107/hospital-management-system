from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .models import Booking, AvailableSlot, User


# Create your views here.

def index(request):
    return render(request, 'booking_system/index.html')




def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        confirm_password = request.POST['confirm']

        role = request.POST['role']
        if role not in ['doctor', 'patient']:
            return render(request, 'booking_system/register.html', {'error': 'Invalid role'})
        if password != confirm_password:
            return render(request, 'booking_system/register.html', {'error': 'Passwords do not match'})
        
        user = User.objects.create_user(username=username, password=password, email=email, role=role)
        login(request, user)
        return HttpResponseRedirect('/')
    return render(request, 'booking_system/register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
        else:
            messages.error(request, "User doesn't exist")
            return render(request, "booking_system/login.html")
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "booking_system/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))