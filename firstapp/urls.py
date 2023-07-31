from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('handle_signup', views.handle_signup, name='handle_signup'), 
    path('handle_login', views.handle_login, name="handle_login"),
    path('handle_logout', views.handle_logout, name="handle_logout"),
    # Other URL patterns for your project
]