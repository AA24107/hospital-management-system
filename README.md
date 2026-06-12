# Mini Hospital Management System (HMS)

A local-first hospital management backend application built with Django, focused on doctor availability management and patient appointment booking with Google Calendar integration.

---

# Features

## Authentication & Roles

* Doctor and Patient sign up/log in
* Password hashing using the Django authentication system
* Role-based access control
* Separate dashboards for doctors and patients

---

## Doctor Functionality

* Create availability slots
* Edit availability slots
* View only their own slots
* Booked slots become unavailable

---

## Patient Functionality

* View available doctor slots
* Book appointments
* Booked slots disappear from availability listings

---

## Race Condition Handling

The booking flow includes transactional protection to reduce the risk of double booking when multiple patients attempt to reserve the same slot simultaneously.

---

## Google Calendar Integration

* OAuth2-based Google Calendar connection
* Calendar events automatically created after successful booking
* Events created in:

  * Doctor calendar
  * Patient calendar

---

# Tech Stack

* Backend Framework: Django
* Database: SQLite
* ORM: Django ORM
* Authentication: Django Auth System
* Google API: Google Calendar API + OAuth2
* Frontend: Django Templates + Bootstrap

---

# Project Structure

```text
your-repo/
├── README.md
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

Create a Google Cloud project and enable Google Calendar API.

Download OAuth credentials JSON file and place it in project root as:

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

# System Architecture

## Authentication & Authorization

The application uses Django’s built-in authentication system with a custom role-based model to separate doctors and patients.

Access restrictions are enforced in views to ensure:

* Doctors cannot perform patient actions
* Patients cannot perform doctor actions

---

## Availability & Booking System

Doctors create availability slots with start and end times.

Patients can only see:

* future slots
* unbooked slots

When a patient books a slot:

1. Slot availability is checked
2. Booking is created
3. The slot is marked as booked
4. Google Calendar events are created

---

## Google Calendar Integration

Users connect their Google accounts through OAuth2.

OAuth credentials are stored locally in the database and used to create calendar events after successful booking.

Events are created separately for:

* doctor
* patient

---

# The Design Decision

## Problem

One important challenge was handling race conditions during appointment booking.

If two patients attempt to book the same slot at nearly the same time, both requests may initially see the slot as available, leading to an inconsistent booking state or double booking.

---

## Option 1 — Simple Application-Level Validation

The simplest approach was:

```python
if not slot.is_booked:
```

Then create the booking.

### Problem

This approach is unsafe under concurrent requests because two users could pass the availability check before the database updates the slot status.

---

## Option 2 — Transaction-Based Booking Protection (Chosen Approach)

The chosen approach used database transactions during the booking process to make booking operations more atomic and reduce inconsistent booking states.

This approach was chosen because:

* It better reflects real backend system design
* It reduces concurrency-related inconsistencies
* It separates validation from persistence logic more safely

Although SQLite has limited concurrency handling compared to PostgreSQL, implementing transactional booking logic still provided a more scalable and architecturally sound approach.

---

# Limitations

## SQLite Limitations

SQLite was used for simplicity and local development. It is not ideal for high-concurrency production workloads.

---

## OAuth Token Storage

OAuth credentials are stored locally in the database and are not encrypted. In production, secure encrypted storage would be necessary.

---

## No HTTPS

The application currently runs locally over HTTP for development purposes. Production deployment would require HTTPS for secure OAuth flows.

---

## Limited Validation

Additional validation, auditing, monitoring, and error handling would be needed for a production-grade system.

---

# Demo Features Shown

* Doctor signup/login
* Patient signup/login
* Doctor slot creation/editing
* Patient appointment booking
* Slot blocking behavior
* Google OAuth flow
* Calendar event creation in both user calendars
* Role-based access restrictions

---

# AI Tool Usage

AI tools, including ChatGPT, were used during development for:

* debugging
* architecture discussion
* OAuth integration guidance
* concurrency handling discussion

Relevant logs are included inside:

```text
ai-tool-usage-log/
```

---

# Future Improvements

* PostgreSQL migration
* Email notification service
* JWT authentication
* API-first architecture
* Better UI/UX
* Deployment support
* Stronger concurrency guarantees
* Encrypted credential storage
