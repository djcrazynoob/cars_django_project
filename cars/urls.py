from django.urls import path
from . import w_api, w_auth, w_pages

urlpatterns = [
    # Главная страница - отображение списка всех автомобилей
    path('', w_pages.home, name='home'),
    # Страница с информацией о автомобиле
    path('car/<int:id>', w_pages.car, name='car'),
    # Страница для создания нового автомобиля
    path('car/create/', w_pages.car_create, name='car_create'),
    # Страница для редактирования или удаления автомобиля
    path('car/update/<int:id>', w_pages.car_update, name='car_update'),
    # Страница для авторизации пользователя
    path('auth/', w_pages.auth, name='auth'),
    # Страница для выхода пользователя из системы
    path('logout/', w_pages.logout_user, name='logout_user'),

    # API/Auth
    # Авторизации пользователя
    path('auth/login/', w_auth.login, name='login'),
    # Регистрации нового пользователя
    path('auth/register/', w_auth.register, name='register'),

    # API/Cars
    # Получение списка всех автомобилей, создание нового автомобиля
    path('api/cars/', w_api.cars, name='cars'),  
    # Автомобиль по id: получение, обновление и удаление
    path('api/cars/<int:id>/', w_api.cars, name='cars'),
    # Получение комментариев к автомобилю и добавления нового комментария
    path('api/cars/<int:id>/comments/', w_api.comments, name='comments'),
]
