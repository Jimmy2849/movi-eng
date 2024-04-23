from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.custom_signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
]