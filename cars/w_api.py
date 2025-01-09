from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Car
from .serializers import CarSerializer, CommentSerializer

# Получение списка всех автомобилей, создание нового автомобиля и обновление существующего автомобиля
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def cars(request, id=None):
    # Обработка GET-запроса для получения всех автомобилей
    if request.method == 'GET' and id is None:
        cars = Car.objects.all()  # Получаем все автомобили из базы данных
        serializer = CarSerializer(cars, many=True)  # Сериализуем список автомобилей
        return Response(serializer.data, status=status.HTTP_200_OK)  # Возвращаем сериализованные данные
    
    # Обработка GET-запроса c id для получения информации о автомобиле
    if request.method == 'GET' and id:
        try:
            car = Car.objects.get(id=id)  # Получаем информацию о автомобиле по id
            serializer = CarSerializer(car)  # Сериализуем объект автомобиля
            return Response(serializer.data, status=status.HTTP_200_OK)  # Возвращаем сериализованные данные
        except Car.DoesNotExist:
            # Если автомобиль не найден, возвращаем ошибку 404
            return Response({"detail": "Автомобиль не найден."}, status=status.HTTP_404_NOT_FOUND)

    # Обработка POST-запроса для создания нового автомобиля
    elif request.method == 'POST':
        # Проверка авторизации
        if not request.user.is_authenticated:
            return Response({"detail": "Авторизация обязательна."}, status=status.HTTP_401_UNAUTHORIZED)

        # Сериализация данных для нового автомобиля
        serializer = CarSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            car = serializer.save(owner=request.user)  # Устанавливаем владельца автомобиля
            return Response(CarSerializer(car).data, status=status.HTTP_201_CREATED)  # Возвращаем созданный автомобиль
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Если данные невалидны, возвращаем ошибку
    
    # Обработка PUT-запроса для обновления автомобиля
    elif request.method == 'PUT':
        try:
            car = Car.objects.get(id=id)  # Получаем информацию о автомобиле по id
        except Car.DoesNotExist:
            # Если автомобиль не найден, возвращаем ошибку 404
            return Response({"detail": "Автомобиль не найден."}, status=status.HTTP_404_NOT_FOUND)
        
        # Проверка, является ли пользователь владельцем автомобиля
        if request.user != car.owner:
            # Если пользователь не владелец, возвращаем ошибку 403
            return Response({"detail": "Вы не можете редактировать данные этого автомобиля."}, status=status.HTTP_403_FORBIDDEN)

        # Сериализуем данные для обновления
        serializer = CarSerializer(car, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # Сохраняем обновленные данные
            return Response(serializer.data, status=status.HTTP_200_OK)  # Возвращаем обновленные данные
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Если данные невалидны, возвращаем ошибку
    
    # Обработка DELETE-запроса для удаления автомобиля
    elif request.method == 'DELETE':
        try:
            car = Car.objects.get(id=id)  # Получаем информацию о автомобиле по id
        except Car.DoesNotExist:
            # Если автомобиль не найден, возвращаем ошибку 404
            return Response({"detail": "Автомобиль не найден."}, status=status.HTTP_404_NOT_FOUND)
            
        # Проверка, является ли пользователь владельцем автомобиля
        if request.user != car.owner:
            # Если пользователь не владелец, возвращаем ошибку 403
            return Response({"detail": "Вы не можете удалить этот автомобиль."}, status=status.HTTP_403_FORBIDDEN)

        car.delete()  # Удаляем автомобиль
        return Response({"detail": "Автомобиль удален."}, status=status.HTTP_204_NO_CONTENT)  # Возвращаем сообщение об удалении

# Запрос комментариев и создание нового комментария
@api_view(['GET', 'POST'])
def comments(request, id):
    try:
        car = Car.objects.get(id=id)  # Получаем информацию о автомобиле по id
    except Car.DoesNotExist:
        # Если автомобиль не найден, возвращаем ошибку 404
        return Response({"detail": "Автомобиль не найден."}, status=status.HTTP_404_NOT_FOUND)

    # Обработка GET-запроса для получения комментариев
    if request.method == 'GET':
        comments = car.comments.all()  # Получаем все комментарии для этого автомобиля
        serializer = CommentSerializer(comments, many=True)  # Сериализуем список комментариев
        return Response(serializer.data, status=status.HTTP_200_OK)  # Возвращаем сериализованные данные

    # Обработка POST-запроса для добавления нового комментария
    elif request.method == 'POST':
        # Проверка авторизации
        if not request.user.is_authenticated:
            return Response({"detail": "Авторизация обязательна."}, status=status.HTTP_401_UNAUTHORIZED)

        # Добавление нового комментария
        serializer = CommentSerializer(data=request.data, context={'car': car, 'request': request})
        if serializer.is_valid():
            serializer.save(car=car)  # Связываем комментарий с автомобилем
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Возвращаем созданный комментарий
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Если данные невалидны, возвращаем ошибку
