from django.urls import path
from . import views

app_name = 'db' # 네임스페이스 추가. streamlit에서 접근 시 'http://your-django-server/<app_namespace>/<endpoint>/' 처럼 직접 지정.
urlpatterns = [
    path('signup', views.custom_signup, name='signup'),
    path('login/', views.custom_login, name='login'),
]