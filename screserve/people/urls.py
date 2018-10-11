from django.urls import path, include
from . import views

urlpatterns = [
    path('client/', views.list_clients, name="list_clients"),
    path('client/create/', views.create_profile, name="create_profile"),
    path('client/update/<int:pk>/', views.update_client, name="update_client"),
    path('client/delete/', views.delete_client, name="delete_client"),
    path('client/status/', views.active_or_block_client, name="active_or_block_client"),
    path('officer/', views.list_officers, name="list_officers"),
    path('officer/create/', views.create_officer, name="create_officer"),
    path('officer/update/<int:pk>/', views.update_officer, name="update_officer"),
    path('officer/delete/', views.delete_officer, name="delete_officer"),
]
