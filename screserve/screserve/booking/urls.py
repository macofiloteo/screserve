from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.list_bookings, name="list_bookings"),
    path('create/', views.create_booking, name="create_booking"),
    path('update/<int:pk>/', views.update_booking, name="update_booking"),
    path('status/', views.update_booking_status, name="update_booking_status"),
    path('get_profile_info_json/<int:pk>/', views.get_profile_info_json, name="get_profile_info_json"),
    path('print_booking_details/', views.print_booking_details, name="print_booking_details")
]
