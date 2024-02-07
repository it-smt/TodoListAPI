from django.contrib.auth import authenticate, login
from users.models import User
from django.db import IntegrityError
from ninja.errors import HttpError
from typing import List

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI

from main.models import Todo
from .decorators import custom_login_required
from .schemas import TodoResponse, TodoCreate, UserLogin, Message, UserCreate, Token
from .utils import generate_auth_token

api = NinjaAPI()


@api.post('/register', response={200: Token, 400: Message})
def register_view(request, body: UserCreate):
    """Функция регистрации пользователя."""
    try:
        user = User.objects.create_user(
            username=body.username,
            first_name=body.first_name,
            last_name=body.last_name,
            email=body.email,
            auth_token=generate_auth_token()
        )
    except IntegrityError:
        return 400, {'detail': 'Пользователь с таким username уже существует.'}
    user.set_password(body.password)
    user.save()
    return {'message': 'Вы успешно зарегистрировались', 'token': user.auth_token}


@api.post('/login', response={200: Token, 400: Message})
def login_view(request, body: UserLogin):
    """Функция авторизации и аутентификации пользователя."""
    user = authenticate(request, username=body.username, password=body.password)

    if user:
        return {'message': 'Вы успешно авторизованы.', 'token': user.auth_token}
    raise HttpError(400, 'Неверный username или password.')


@api.get('/todos', response={200: List[TodoResponse], 404: Message, 401: Message})
@custom_login_required
def get_todos(request):
    """Функция для получения всех задач пользователя, которые еще не выполнены."""
    token = request.headers.get('Authorization', '')
    user = User.objects.get(auth_token=token)
    todos = Todo.objects.filter(user=user, status=Todo.Status.NOT_DONE).values()
    if todos.count() <= 0:
        raise HttpError(404, 'Задач пока что нет.')
    return todos


@api.post('/create_todo', response={201: TodoResponse, 401: Message})
@custom_login_required
def create_todo(request, todo_scheme: TodoCreate):
    """Функция для создания задачи."""
    token = request.headers.get('Authorization', '')
    user = User.objects.get(auth_token=token)
    todo = Todo.objects.create(
        user=user,
        title=todo_scheme.title,
        description=todo_scheme.description,
    )
    return 201, TodoResponse.from_orm(todo)


@api.patch('/edit_todo/{todo_id}', response={200: TodoResponse, 401: Message})
@custom_login_required
def edit_todo(request, todo_id: int, body: TodoCreate):
    """Функция для редактирования задачи."""
    token = request.headers.get('Authorization', '')
    user = User.objects.get(auth_token=token)
    todo = get_object_or_404(Todo, id=todo_id, user=user, status=Todo.Status.NOT_DONE)
    todo.title = body.title
    todo.description = body.description
    todo.save()
    return TodoResponse.from_orm(todo)


@api.patch('/edit_status_todo_on_done/{todo_id}', response={200: Message, 401: Message})
@custom_login_required
def edit_status_order_on_done(request, todo_id: int):
    """Функция для изменения статуса задачи на 'Готово'."""
    token = request.headers.get('Authorization', '')
    user = User.objects.get(auth_token=token)
    todo = get_object_or_404(Todo, id=todo_id, user=user, status=Todo.Status.NOT_DONE)
    todo.status = Todo.Status.DONE
    todo.save()
    return {'detail': f'Статус для задачи с id {todo.id} успешно изменен.'}
