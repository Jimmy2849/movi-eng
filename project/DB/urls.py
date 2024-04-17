from django.urls import path
from .views import custom_signup, custom_login

app_name = 'db' # 네임스페이스 추가. streamlit에서 접근 시 'http://your-django-server/<app_namespace>/<endpoint>/' 처럼 직접 지정.
urlpatterns = [
    path('/signup', custom_signup),
    path('/login/', custom_login),
]