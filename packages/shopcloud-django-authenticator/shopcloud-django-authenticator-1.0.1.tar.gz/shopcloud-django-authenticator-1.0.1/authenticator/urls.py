from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = routers.SimpleRouter()

urlpatterns = [
    path('login', views.login_view, name='authenticator-login'),
]
urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
