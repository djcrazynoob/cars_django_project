from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    make = models.CharField(max_length=100)  # Марка автомобиля
    model = models.CharField(max_length=100)  # Модель автомобиля
    year = models.PositiveIntegerField()  # Год выпуска
    description = models.TextField()  # Описание автомобиля
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания
    updated_at = models.DateTimeField(auto_now=True)  # Дата и время последнего обновления
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Внешний ключ на создателя

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


class Comment(models.Model):
    content = models.TextField()  # Содержание комментария
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания
    car = models.ForeignKey(Car, related_name="comments", on_delete=models.CASCADE)  # Внешний ключ на автомобиль
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Внешний ключ на комментатора

    def __str__(self):
        return f"Комментарий от {self.author} к автомобилю {self.car}"