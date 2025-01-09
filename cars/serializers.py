from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token 
from .models import Car, Comment

# Сериализатор для пользователя
class UserSerializer(serializers.ModelSerializer):
    # Пароль только для записи
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    # Метод для создания пользователя с зашифрованным паролем
    def create(self, validated_data):
        # Извлекаем пароль из данных
        password = validated_data.pop('password')
        # Создаем пользователя без пароля
        user = User(**validated_data)
        # Устанавливаем зашифрованный пароль
        user.set_password(password)
        # Сохраняем пользователя
        user.save()
        return user
    
# Сериализатор для авторизации пользователя
class UserLoginSerializer(serializers.Serializer):
    # Параметры для авторизации (логин и пароль)
    username = serializers.CharField()
    password = serializers.CharField()

    # Проверка правильности введенных данных
    def validate(self, data):
        # Ищем пользователя по имени
        user = User.objects.filter(username=data['username']).first()
        # Проверяем, существует ли пользователь и совпадает ли пароль
        if not user or not user.check_password(data['password']):
            raise serializers.ValidationError("Неверный логин или пароль.")

        # Генерация токена для авторизованного пользователя
        token, created = Token.objects.get_or_create(user=user)
        # Возвращаем сгенерированный токен
        return {'token': token.key}


# Сериализатор для автомобиля
class CarSerializer(serializers.ModelSerializer):
    # Информация о владельце автомобиля, используется сериализатор пользователя
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'year', 'description', 'created_at', 'updated_at', 'owner']

    # Метод для создания нового автомобиля
    def create(self, validated_data):
        # Устанавливаем владельца автомобиля как текущего авторизованного пользователя
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    # Метод для обновления автомобиля
    def update(self, instance, validated_data):
        # Проверка, является ли пользователь владельцем автомобиля
        if self.context['request'].user != instance.owner:
            raise serializers.ValidationError("Вы не можете редактировать данные этого автомобиля.")
        # Выполняем обновление
        return super().update(instance, validated_data)

# Сериализатор для комментариев
class CommentSerializer(serializers.ModelSerializer):
    # Автор комментария, отображается как имя пользователя
    author = serializers.StringRelatedField(read_only=True)
    # Автомобиль, к которому относится комментарий
    car = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'car', 'author']

    # Метод для создания нового комментария
    def create(self, validated_data):
        # Извлекаем автомобиль, к которому относится комментарий
        car = self.context['car']
        # Устанавливаем пользователя как автора комментария
        validated_data['author'] = self.context['request'].user
        # Устанавливаем автомобиль, к которому привязан комментарий
        validated_data['car'] = car
        # Создаем новый комментарий
        return super().create(validated_data)
