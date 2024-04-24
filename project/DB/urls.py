from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.custom_signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('save_word/', views.save_word, name='save_word'),
    path('count_word/', views.count_word, name='count_word'),
]