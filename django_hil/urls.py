"""
URL configuration for django_hil project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
import users.views
import booking.views
import trainer.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('booking/', include('booking.urls')),
    path('trainer/', include('trainer.urls')),
    
    path('login/', users.views.login_page, name='login_page'),
    path('logout/', users.views.logout_page, name='logout_page'),
    path('register/', users.views.register_page, name='register_page'),
    
    path('booking_page', booking.views.booking_page, name='booking_page'),
    path('booking/<int:booking_id>', booking.views.specific_booking, name='specific_booking'),
    path('booking/<int:booking_id>/accept/', booking.views.accept_booking, name='accept_booking'),
    path('booking/<int:booking_id>/cancel/', booking.views.cancel_booking, name='cancel_booking'),
    
    path('trainer_page', trainer.views.trainer_page, name='trainer_page'),
    path('trainer/<int:category_id>', trainer.views.category_page, name='category_page'),
    path('trainer/<int:trainer_id>', trainer.views.specific_trainer, name='specific_trainer'),
    path('trainer/<int:trainer_id>/accept/', trainer.views.trainer_service_booking, name='trainer_service_booking'),
    path('trainer/<int:trainer_id>/service/', trainer.views.trainer_service, name='trainer_service_cancel'),
    path('trainer_registratione/', trainer.views.trainer_registratione, name='trainer_registratione'),    
    
]
