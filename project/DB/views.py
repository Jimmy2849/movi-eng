from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# 사용자가 입력한 username를 data로 받음, 응답으로 'success'와 'token'을 json으로 반환해야 함.
# https://docs.djangoproject.com/en/5.0/ref/contrib/auth/#django.contrib.auth.models.User 
# https://www.django-rest-framework.org/api-guide/authentication/

@csrf_exempt
def custom_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(f'username : {username} \n password : {password}')
        # 이미 존재하는 사용자명인지 확인
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'}, status=400)
        
        # 사용자 생성
        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({'success': True}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 회원명을 기반으로 사용자를 검색합니다.
        user = authenticate(username=username, password=password)

        if user is not None:
            # 사용자를 로그인합니다.
            login(request, user)
            token = get_token();
            return JsonResponse({'success': True, 'token': token}, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid ID.'}, status=400)

    return JsonResponse({'success': False, 'error': 'Method not allowed.'}, status=405)
    