from django.urls import path
from . import views

urlpatterns = [
    path('user', views.user_page, name='user_page'),
    path('/login', views.login_page, name='login_page'),
    path('/logout', views.logout_page, name='logout_page'),
    path('/register', views.register_page, name='register_page'),
    path('/user/<int:user_id>', views.specific_user, name='user_specific'),
]