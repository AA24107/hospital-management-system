from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone

from .models import Booking, AvailableSlot, User


# Create your views here.
def index(request):
    available_slots = AvailableSlot.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
    return render(request, 'booking_system/index.html', {'available_slots': available_slots})


@login_required
def create_slots(request):
    if request.user.role != 'doctor':  
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        doctor = request.user
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        
        if not start_time or not end_time:
            return render(request, 'booking_system/create_slots.html', {'error': 'Start time and end time are required'})
        elif start_time >= end_time:
            return render(request, 'booking_system/create_slots.html', {'error': 'Start time must be before end time'})
        
        AvailableSlot.objects.create(doctor=doctor, start_time=start_time, end_time=end_time)
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'booking_system/create_slots.html')


@login_required
def slot_detail(request, slot_id):
    slot = AvailableSlot.objects.get(id=slot_id)
    return render(request, 'booking_system/slot_detail.html', {'slot': slot})

@login_required
def book_slot(request, slot_id):
    if request.user.role != 'patient':
        return HttpResponseRedirect(reverse('index'))
    
    slot = AvailableSlot.objects.get(id=slot_id)
    if slot.is_booked:
        messages.error(request, 'This slot is already booked')
        return HttpResponseRedirect(reverse('index'))
    
    Booking.objects.create(doctor=slot.doctor, patient=request.user, slot=slot)
    slot.is_booked = True
    slot.save()
    return HttpResponseRedirect(reverse('index'))


@login_required
def edit_slot(request, slot_id):
    slot = AvailableSlot.objects.get(id=slot_id)
    if request.user != slot.doctor:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'POST':
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        
        if not start_time or not end_time:
            return render(request, 'booking_system/edit_slot.html', {'slot': slot, 'error': 'Start time and end time are required'})
        elif start_time >= end_time:
            return render(request, 'booking_system/edit_slot.html', {'slot': slot, 'error': 'Start time must be before end time'})
        
        slot.start_time = start_time
        slot.end_time = end_time
        slot.save()
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'booking_system/edit_slot.html', {'slot': slot})


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