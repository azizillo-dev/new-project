from django.shortcuts import render
from .serializers import ProfileUpdateSerializer, SignUpserializer, PasswordChangeSerializer, \
    LoginSerializer, ChangePhotoSerializer
from rest_framework.response import Response
from .models import CustomUser, Verify, NEW, CODE_VERIFY, VIA_EMAIL, VIA_PHONE
from .mailer import send_verification_code
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import permissions
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.


class SignUpView(CreateAPIView):
    serializer_class = SignUpserializer
    queryset = CustomUser.objects.all()
    
    
class VerifyCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        code = request.data.get('code')
        user = request.user
        
        current_code = user.codes.all().filter(code=code, used=False, expire_time__gte=datetime.now()).first()
        
        if current_code is None:
            raise ValidationError('Kod xato yoki eskirgan')

        if user.auth_status == NEW:
            current_code.used = True
            current_code.save()
            
            user.auth_status = CODE_VERIFY
            user.save()
                        
        return Response({
            'auth_status': user.auth_status,
            'msg': "code_verify"
        })
        
        
class GetNewCodeView(APIView):
    def get(self, request):
        user = request.user
        codes = user.codes.all().filter(used=False, expire_time__gte=datetime.now()).exists()
        if codes:
            raise ValidationError('Sizda hali activa kod bor')
        
        if user.auth_status == NEW:
            if user.auth_type == VIA_EMAIL:
                code = user.generate_code(user.auth_type)
                send_verification_code(user.email, code)
                
            elif user.auth_type == VIA_PHONE:
                code = user.generate_code(user.auth_type)
                send_verification_code(user.phone_number, code) 
            return Response({
                "msg": 'Code yuborildi',
                'auth_type': user.auth_type
            })
            
        return Response({
            "msg": 'Siz oldin email yoki telefon raqam kiriting',
            'auth_type': user.auth_type
        })
        
    
class ChangePhotoView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePhotoSerializer
    queryset = CustomUser.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    
    def get_object(self):
        return self.request.user    

    
class TokenRefreshView(APIView):
    def get(self, request):
        refresh = request.data.get('refresh')
        try:
            refresh_token = RefreshToken(refresh)
        except:
            raise ValidationError('Token eskirgan yoki xato')
        
        return Response({
            'access': str(refresh_token.access_token)
        })
        
        
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serialzier = LoginSerializer(data=request.data)
        serialzier.is_valid(raise_exception=True)
        return Response(serialzier.data)
        
        
    
class ProfileUpdateView():
    def patch(self, request):
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class PasswordChangeView():
    def put(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        return Response({'detail': 'Parol muvaffaqiyatli o\'zgartirildi.'})
    

class LogoutView():
    def post(self, request):
        refresh_token = request.data.get('refresh')
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            raise ValidationError('Token eskirgan yoki xato')
        
        return Response({'detail': 'Muvaffaqiyatli chiqildi.'})




