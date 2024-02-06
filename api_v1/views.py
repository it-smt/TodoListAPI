from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from ninja.errors import HttpError
from typing import List, Dict

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI

from main.models import Todo
from .schemas import TodoResponse, TodoCreate, UserLogin, Message, UserCreate

api = NinjaAPI()


@api.post('/register', response={200: Message, 400: Message})
def register_view(request, body: UserCreate):
    """Функция регистрации пользователя."""
    try:
        user = User.objects.create_user(
            username=body.username,
            first_name=body.first_name,
            last_name=body.last_name,
            email=body.email,
        )
    except IntegrityError:
        return 400, {'detail': 'Пользователь с таким username уже существует.'}
    user.set_password(body.password)
    user.save()
    return {'detail': 'Вы успешно зарегистрировались. Теперь вы можете авторизоваться в системе.'}


@api.post('/login', response={200: Message, 401: Message})
def login_view(request, body: UserLogin):
    """Функция авторизации и аутентификации пользователя."""
    user = authenticate(request, username=body.username, password=body.password)

    if user:
        login(request, user)
        return {'detail': 'Вы успешно авторизованы.'}
    raise HttpError(401, 'Неверный username или password.')


@api.post('/logout', response={200: Message, 401: Message})
def logout_view(request):
    """Функция выхода пользователя."""
    if not request.user.is_anonymous:
        logout(request)
        return {'detail': 'Вы успешно вышли.'}
    return 401, {'detail': 'Для выхода нужно авторизоваться.'}


@api.get('/todos', response={200: List[TodoResponse], 404: Dict})
@login_required
def get_todos(request):
    """Функция для получения всех задач пользователя, которые еще не выполнены."""
    todos = Todo.objects.filter(user=request.user, status=Todo.Status.NOT_DONE).values()
    if todos.count() <= 0:
        raise HttpError(404, 'Задач пока что нет.')
    return todos


@api.post('/create_todo', response={201: TodoResponse})
@login_required
def create_todo(request, todo_scheme: TodoCreate):
    """Функция для создания задачи."""
    todo = Todo.objects.create(
        user=request.user,
        title=todo_scheme.title,
        description=todo_scheme.description,
    )
    return TodoResponse.from_orm(todo)


@api.patch('/edit_todo/{todo_id}', response={200: TodoResponse})
@login_required
def edit_todo(request, todo_id: int, body: TodoCreate):
    """Функция для редактирования задачи."""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user, status=Todo.Status.NOT_DONE)
    todo.title = body.title
    todo.description = body.description
    todo.save()
    return TodoResponse.from_orm(todo)


@api.patch('/edit_status_todo_on_done/{todo_id}', response={200: Message})
@login_required
def edit_status_order_on_done(request, todo_id: int):
    """Функция для изменения статуса задачи на 'Готово'."""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user, status=Todo.Status.NOT_DONE)
    todo.status = Todo.Status.DONE
    todo.save()
    return {'detail': f'Статус для задачи с id {todo.id} успешно изменен.'}
