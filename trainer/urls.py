from django.urls import path
from . import views

urlpatterns = [
    path('', views.trainer_page, name='trainer_page'),
    path('category_page/', views.category_page, name='category_page'),
    path('specific_trainer/', views.specific_trainer, name='specific_trainer'),
    path('service/', views.trainer_service, name='trainer_service'),
    path('<int:trainer_id>/<int:service_id>/', views.trainer_service_page, name='trainer_service_page'),
    path('registratione/', views.trainer_registratione, name='trainer_registration'),
    path('<int:trainer_id>/', views.trainer_details, name='trainer_details'),
]
