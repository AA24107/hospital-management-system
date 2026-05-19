from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('slot/<int:slot_id>/', views.slot_detail, name='slot_detail'),
    path('create_slots/', views.create_slots, name='create_slots'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('book/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('edit/<int:slot_id>/', views.edit_slot, name='edit_slot'),
    path('dashboard/', views.dashboard, name='dashboard'),
]