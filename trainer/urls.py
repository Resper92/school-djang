from django.urls import path
from . import views

urlpatterns = [
    path('/trainer/',view=views.trainer_page, name='trainer_page'),
    path('/trainer/<int:category_id>',view=views.category_page, name='category_page'),
    path('/trainer/<int:trainer_id>',view=views.specific_trainer, name='specific_trainer'),
    path('/trainer/<int:trainer_id>/service',view=views.trainer_service, name='trainer_service'),
    path('/trainer/<int:trainer_id>/booking',view=views.trainer_service_booking, name='trainer_service_booking'),
    path('/trainer_registratione/',view=views.trainer_registratione, name='trainer_registratione'),
]