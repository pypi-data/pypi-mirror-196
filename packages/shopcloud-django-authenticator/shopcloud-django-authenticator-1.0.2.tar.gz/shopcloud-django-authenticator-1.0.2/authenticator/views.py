import jwt
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


def login_view(request):
    token = request.GET.get('token')
    if token is None:
        return HttpResponseUnauthorized()

    if settings.AUTHENTICATOR_KEY is None:
        return HttpResponseUnauthorized()

    data = jwt.decode(
        token,
        settings.AUTHENTICATOR_KEY,
        algorithms="HS256",
        options={
            "require": [
                "exp",
                "iss",
                "nbf"
            ]
        }
    )
    if data.get('iss') != 'shopcloud-secrethub':
        return HttpResponseUnauthorized()

    user = User.objects.filter(username=data.get('username')).first()
    password = User.objects.make_random_password()
    if user is None:
        user = User.objects.create(
            username=data.get('username'),
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True if "admin" in data.get('scopes', []) else False
        user.save()
    else:
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True if "admin" in data.get('scopes', []) else False
        user.save()

    login(request, user)

    return redirect('/', permanent=False)
