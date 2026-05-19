from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bookings/', views.bookings, name='bookings'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]