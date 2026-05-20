from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
import os
from google_auth_oauthlib.flow import Flow

from .models import Booking, AvailableSlot, User, GoogleCredentials
from .google_calendar import create_event_for_user

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Create your views here.
def index(request):
    available_slots = AvailableSlot.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
    return render(request, 'booking_system/index.html', {'available_slots': available_slots})


@login_required
def dashboard(request):
    available_slots = AvailableSlot.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
    available_slots = available_slots.filter(doctor=request.user) if request.user.role == 'doctor' else available_slots
    patient_bookings = Booking.objects.filter(patient=request.user).select_related('slot', 'doctor')
    google_creds = GoogleCredentials.objects.filter(user=request.user).first()
    return render(request, 'booking_system/dashboard.html', {
        'available_slots': available_slots,
        'patient_bookings': patient_bookings,
        'google_creds': google_creds
    })


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
    with transaction.atomic():
        if request.user.role != 'patient':
            return HttpResponseRedirect(reverse('index'))
        
        slot = AvailableSlot.objects.select_for_update().get(id=slot_id)
        slot = get_object_or_404(AvailableSlot.objects.select_for_update(), id=slot_id)
        if slot.is_booked:
            messages.error(request, 'This slot is already booked')
            return HttpResponseRedirect(reverse('index'))
        
        Booking.objects.create(doctor=slot.doctor, patient=request.user, slot=slot)
        slot.is_booked = True
        slot.save()
        try:
            event = {
                "summary": f"Appointment with Dr. {slot.doctor.username}",
                "description": f"Patient: {request.user.username}",
                "start": {
                    "dateTime": slot.start_time.isoformat(),
                    "timeZone": "Asia/Kolkata",
                },
                "end": {
                    "dateTime": slot.end_time.isoformat(),
                    "timeZone": "Asia/Kolkata",
                },
            }
            create_event_for_user(slot.doctor, event)
            create_event_for_user(request.user, event)
    
        except Exception as e:
            messages.error(request, 'Error occurred while creating Google Calendar event')
            slot.is_booked = False

        return HttpResponseRedirect(reverse('index'))


@login_required
def google_connect(request):

    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/calendar"]
    )

    flow.redirect_uri = "http://127.0.0.1:8000/google/callback/"

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )

    request.session["state"] = state
    request.session["code_verifier"] = flow.code_verifier

    return redirect(authorization_url)


@login_required
def google_callback(request):

    state = request.session["state"]
    code_verifier = request.session["code_verifier"]

    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/calendar"],
        state=state
    )

    flow.redirect_uri = "http://127.0.0.1:8000/google/callback/"

    flow.code_verifier = code_verifier

    flow.fetch_token(
        authorization_response=request.build_absolute_uri()
    )

    creds = flow.credentials

    GoogleCredentials.objects.update_or_create(
        user=request.user,
        defaults={
            "access_token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": " ".join(creds.scopes),
        }
    )

    return redirect("index")

@login_required
def edit_slot(request, slot_id):
    slot = AvailableSlot.objects.get(id=slot_id)
    if request.user != slot.doctor or slot.is_booked:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        slot.start_time = start_time
        slot.end_time = end_time
        if not slot.start_time or not slot.end_time:
            return render(request, 'booking_system/create_slots.html', {'slot': slot, 'error': 'Start time and end time are required'})
        elif slot.start_time >= slot.end_time:
            return render(request, 'booking_system/create_slots.html', {'slot': slot, 'error': 'Start time must be before end time'})
        else:
            slot.save()
            return HttpResponseRedirect(reverse('index'))

    return render(request, 'booking_system/create_slots.html', {'slot': slot})


@login_required
def delete_slot(request, slot_id):
    slot = AvailableSlot.objects.select_for_update().get(id=slot_id)
    if request.user != slot.doctor or slot.is_booked:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'POST':
        slot.delete()
        return HttpResponseRedirect(reverse('index'))

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