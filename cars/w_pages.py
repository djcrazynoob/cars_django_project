from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import User, Car, Comment
from .forms import CarForm

# Главная страница - отображение списка всех автомобилей
def home(request):
    cars = Car.objects.all()  # Получаем все автомобили
    return render(request, 'home.html', {'cars': cars})  # Отображаем страницу

# Страница с информацией о автомобиле
def car(request, id):
    try:
        car = Car.objects.get(id=id)  # Получаем автомобиль по его ID
        comments = Comment.objects.filter(car=car).order_by('-created_at')  # Получаем все комментарии к автомобилю

        # Проверка, POST запроса с комментарием
        if request.method == 'POST' and request.user.is_authenticated:
            content = request.POST.get('content')  # Получаем содержимое комментария из формы
            if content:  # Если комментарий не пустой
                Comment.objects.create(car=car, author=request.user, content=content)  # Создаем новый комментарий
                return redirect('car', id=car.id)  # Перенаправляем на страницу автомобиля, чтобы отобразить новый комментарий
        
        # Отображаем страницу с информацией о автомобиле и его комментариях
        return render(request, 'car_detail.html', {'car': car, 'comments': comments})

    except Car.DoesNotExist:
        # Если автомобиль с таким ID не найден, отображаем ошибку
        return render(request, 'car_detail.html', {'error_message': 'Автомобиль не найден.'})

# Страница для создания нового автомобиля
@login_required
def car_create(request):
    # Если форма отправлена методом POST
    if request.method == "POST":
        form = CarForm(request.POST)  # Инициализируем форму с данными из запроса
        if form.is_valid():
            car = form.save(commit=False)  # Сохраняем объект автомобиля
            car.owner = request.user  # Устанавливаем владельца автомобиля
            car.save()  # Сохраняем автомобиль в базу данных

            # Перенаправление на страницу нового автомобиля
            return redirect('car', id=car.id)
    else:
        form = CarForm()

    return render(request, 'car_create.html', {'form': form})  # Отображаем форму для создания автомобиля

# Страница изменения автомобиля
@login_required
def car_update(request, id):
    try:
        car = Car.objects.get(id=id)  # Получаем автомобиль по его ID

        # Проверка, что пользователь является владельцем автомобиля
        if request.user != car.owner:
            return redirect('car', id=id)  # Если пользователь не является владельцем, перенаправляем на страницу автомобиля

        # Если форма отправлена методом POST
        if request.method == 'POST':
            # Если нажата кнопка "Удалить"
            if 'delete' in request.POST:
                car.delete()  # Удаляем автомобиль из базы данных
                return redirect('home')  # Перенаправляем на главную страницу, где отображаются все автомобили

            # Если нажата кнопка "Обновить"
            form = CarForm(request.POST, instance=car)  # Инициализируем форму с текущими данными автомобиля
            if form.is_valid():  # Если форма прошла валидацию
                form.save()  # Сохраняем обновленные данные автомобиля
                return redirect('car', id=car.id)  # Перенаправляем на страницу обновленного автомобиля
        else:
            form = CarForm(instance=car)  # Загружаем текущие данные автомобиля в форму для редактирования

        return render(request, 'car_update.html', {'form': form, 'car': car})  # Отображаем форму для обновления автомобиля
    except Car.DoesNotExist:
        # Если автомобиль с таким ID не найден, отображаем ошибку
        return render(request, 'car_update.html', {'error_message': 'Автомобиль не найден.'})


# Авторизация
def auth(request, error_message=None):
    # Если форма отправлена методом POST
    if request.method == "POST":
        # Если пользователь пытается авторизоваться
        if 'login' in request.POST:
            username = request.POST['username']  # Получаем имя пользователя из формы
            password = request.POST['password']  # Получаем пароль из формы
            user = authenticate(username=username, password=password)  # Проверяем данные пользователя

            if user is not None:  # Если пользователь найден
                login(request, user)  # Авторизуем пользователя
                return redirect('home')  # Перенаправляем на главную страницу
            else:
                error_message = "Неверный логин или пароль."  # Если аутентификация не удалась, отображаем сообщение об ошибке

        # Если пользователь пытается зарегистрироваться
        elif 'register' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']

            # Проверяем, что пароли совпадают
            if password != password_confirm:
                error_message = "Пароли не совпадают."
            else:
                # Проверяем, существует ли пользователь с таким именем
                if User.objects.filter(username=username).exists():
                    error_message = "Пользователь с таким именем уже существует."
                else:
                    # Создаем нового пользователя
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    # После регистрации сразу авторизуем пользователя
                    login(request, user)
                    return redirect('home')  # Перенаправляем на главную страницу

    return render(request, 'auth.html', {'error_message': error_message})  # Отображаем страницу с формой

# Выход из аккаунта
def logout_user(request):
    logout(request)  # Выход из текущей сессии пользователя
    return redirect('home')  # Перенаправляем на главную страницу после выхода
