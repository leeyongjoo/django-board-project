from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import CustomLoginView

app_name = "common"

urlpatterns = [
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('signup', views.signup, name='signup')
]