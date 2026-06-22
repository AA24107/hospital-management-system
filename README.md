# Hospital Management System (HMS)

A Django-based hospital management backend application for managing doctor availability, patient appointments, and calendar scheduling.

Built with a focus on authentication, role-based access control, booking workflows, API integration, and backend design practices.

---

# Demo

[![Watch the demo](https://img.youtube.com/vi/FJY4YVim_y0/0.jpg)](https://youtu.be/FJY4YVim_y0)

The demo covers:

- Doctor registration and login
- Patient registration and login
- Doctor availability management
- Appointment booking flow
- Slot availability updates
- Google Calendar integration
- Role-based dashboard access

---

# Features

## Authentication & Authorization

- Doctor and patient authentication
- Django-based authentication system
- Role-based access control
- Separate dashboards and workflows

---

## Doctor Features

Doctors can:

- Create availability slots
- Edit existing slots
- View their own schedules
- Manage appointment availability

Booked slots are automatically removed from available listings.

---

## Patient Features

Patients can:

- View available doctor slots
- Book appointments
- Receive calendar events after successful booking

---

## Appointment Booking System

The booking workflow uses database transactions to improve consistency and reduce double-booking issues during concurrent booking attempts.

Booking flow:

1. Patient selects an available slot
2. Availability is validated
3. Appointment is created
4. Slot status is updated
5. Calendar events are generated

---

# Google Calendar Integration

Integrated Google Calendar API using OAuth2 authentication.

After successful booking:

- Event is created in the doctor's calendar
- Event is created in the patient's calendar

---

# Tech Stack

**Backend**
- Django
- Django ORM
- SQLite

**Authentication**
- Django Authentication System

**APIs**
- Google Calendar API
- OAuth2

**Frontend**
- Django Templates
- Bootstrap

---

# Project Structure

```text
hospital-management-system/
|
├── booking_system/
├── HMS/
├── manage.py
├── requirements.txt
└── credentials.json (excluded from git)
```

---

# Setup and Run

## 1. Clone Repository

```bash
git clone https://github.com/AA24107/hospital-management-system
cd hospital-management-system
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
.\venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Google OAuth

Create a Google Cloud project and enable the Google Calendar API.

Download the OAuth credentials JSON file and place it in the project root as:

```text
credentials.json
```

Add the following redirect URI in Google Cloud Console:

```text
http://127.0.0.1:8000/google/callback/
```

---

## 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6. Run Server

```bash
python manage.py runserver
```

Application runs locally at:

```text
http://127.0.0.1:8000/
```

---

# Design Decisions

## Handling Booking Conflicts

A simple availability check:

```python
if not slot.is_booked:
````
It can fail when multiple users attempt to book the same slot at the same time.

To improve reliability, the booking process uses database transactions to make the operation more atomic and reduce inconsistent booking states.

SQLite was used for local development. A production deployment would typically use PostgreSQL for better concurrency handling and scalability.

---

# Limitations

* SQLite is used for local development and is not ideal for high-concurrency production workloads
* OAuth credentials require secure, encrypted storage in production environments
* HTTPS would be required for secure production OAuth flows
* Additional monitoring, logging, validation, and error handling would be needed for a production-grade system

---

# Future Improvements

* PostgreSQL migration
* REST API implementation
* JWT-based authentication
* Email notification system
* Production deployment
* Improved UI/UX
* Stronger security practices

---

# Learning Outcomes

Through this project, I explored:

* Backend architecture using Django
* Authentication and authorization systems
* Database modeling and ORM usage
* Third-party API integration
* OAuth2 authentication flow
* Handling real-world booking consistency problems
