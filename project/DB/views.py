from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from DB.models import Dictionary

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

@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 회원명을 기반으로 사용자를 검색합니다.
        user = authenticate(username=username, password=password)
        if user is not None:
            # 사용자를 로그인합니다.
            login(request, user)
            return JsonResponse({'success': True, 'userid': userid}, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid ID.'}, status=400)

    return JsonResponse({'success': False, 'error': 'Method not allowed.'}, status=405)
    
@csrf_exempt
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True}, status=200)
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed.'}, status=405)

# username으로 userid를 찾아 외래키에 저장
# 중복된 단어검색 소요 시간 -> 인덱스?
@csrf_exempt
def save_word(request):
    if request.method == 'POST':
        word = request.POST.get('word')
        meaning = request.POST.get('meaning')
        userid = request.POST.get('userid')
        print(f'userid: {userid}\n word: {word}\n meaning: {meaning}\n')
        word_obj, created = Dictionary.objects.get_or_create(word=word, userid=User(id=userid), defaults={"meaning": meaning},)
        if created:
            print("created: True")
            word_obj.save()
            return JsonResponse({'success': True, 'message': f"단어 '{word}'를 데이터베이스에 저장했습니다."})
        else:
            return JsonResponse({'success': False, 'message': f"단어 '{word}'는 이미 데이터베이스에 존재합니다."})
    return

# 참조하는 userid에 해당하는 단어장 출력
# Select * from Dict
# Select Count(*) from Dict
@csrf_exempt
def select_word(request):
    return Dictionary.objects.all()