from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("registration", views.RegistrationView.as_view(), name="registration"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("userList/", login_required(views.UserView.as_view()), name="userList"),
]
