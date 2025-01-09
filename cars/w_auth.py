from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, UserLoginSerializer

# Регистрация нового пользователя
@api_view(['POST'])
def register(request):
    # Инициализация сериализатора для регистрации нового пользователя
    serializer = UserSerializer(data=request.data)
    
    # Проверка валидности данных
    if serializer.is_valid():
        # Сохранение нового пользователя
        user = serializer.save()
        
        # Генерация токена авторизации для нового пользователя
        token, created = Token.objects.get_or_create(user=user)
        
        # Возвращаем токен в ответе
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)
    
    # Если данные не прошли валидацию, возвращаем ошибку
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Авторизация существующего пользователя
@api_view(['POST'])
def login(request):
    # Инициализация сериализатора для авторизации пользователя
    serializer = UserLoginSerializer(data=request.data)
    
    # Проверка валидности данных
    if serializer.is_valid():
        # Возвращаем данные пользователя и токен
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    # Если данные не прошли валидацию, возвращаем ошибку
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
