from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class MyProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # request.user에 접근하여 토큰 검증
            userid = request.user.id
            content = {'success': True, 'userid': userid}
            return Response(content, status=200)
        except Exception as e:
            # JWT 토큰 검증 실패 시
            return Response({'error': 'Invalid or expired token'}, status=401)