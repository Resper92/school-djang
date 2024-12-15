from django.urls import path
from . import views

urlpatterns = [
    path(view=views.trainer_page, name='trainer_page'),
    path(view=views.category_page, name='category_page'),
    path(view=views.specific_trainer, name='specific_trainer'),
    path(view=views.trainer_service, name='trainer_service'),
    path(view=views.trainer_service_booking, name='trainer_service_booking'),
]