from django.urls import path
from . import views

urlpatterns = [
    path('/booking/', views.booking_page, name='booking_page'),
    path('/booking/<int:booking_id>', views.specific_booking, name='booking_specific'),
    path('/booking/<int:booking_id>/delete', views.cancel_booking, name='cancel_booking'),
    path('/booking/<int:booking_id>/edit', views.accept_booking, name='accept_booking'),
]