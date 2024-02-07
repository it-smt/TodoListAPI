import secrets


def generate_auth_token():
    # Генерируем случайную строку
    token = ''.join(
        secrets.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(256))
    return token
