from functools import wraps

from ninja.errors import HttpError


def custom_login_required(view_func):
    """

    Декоратор схожий с login_required,
    но он не перенаправляет на другую страницу,
    а выдает ошибку в случае, если пользователь не авторизован.

    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise HttpError(401, 'Не авторизован.')
        return view_func(request, *args, **kwargs)

    return _wrapped_view
