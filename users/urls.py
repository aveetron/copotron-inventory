from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.RegistrationView.as_view(), name='registration'),
    path('login', views.LoginView.as_view(), name='login'),
    path('loginCheck', views.LoginView.as_view(), name='loginCheck'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('loginPage', views.LoginView.as_view(), name='loginPage'),
    path('userList/', views.UserView.as_view(), name='userList'),
    path('rolePermissionView/', views.UserView.as_view(),
         name='rolePermissionView'),
    path('rolePermissionUpdate/', views.RolePermissionUpdateView.as_view(),
         name='rolePermissionUpdate'),
]
