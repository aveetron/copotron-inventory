from django.shortcuts import render, redirect
import datetime
from datetime import datetime
from users.models import AuthUser
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import auth
from django.contrib import messages
from item.views import DashboardView
from django.views.generic import View
from django.views.decorators.csrf import *
from django.http import JsonResponse


class LoginView(View):
    template_name = "users/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")
            if email and password:
                user = AuthUser.objects.filter(email=email, password=password).last()
                if user is not None:
                    auth_login(request, user)
                    user.save()
                    message = "you are successfully logged in"
                    messages.success(request, message)
                    return redirect("dashboard")
                else:
                    return redirect("login")
            else:
                print("login failed")
                return redirect("login")
        except:
            message = "login failed"
            messages.warning(request, message)
            return redirect("login")


class RegistrationView(DashboardView):
    template_name = "users/registration.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        email = request.POST.get("email")
        passwordOne = request.POST.get("passwordOne")
        passwordTwo = request.POST.get("passwordTwo")
        username = firstName + lastName
        lastLogin = datetime.now()
        dateJoined = datetime.now()
        if passwordOne == passwordTwo:
            user = AuthUser(
                username=username,
                first_name=firstName,
                last_name=lastName,
                email=email,
                is_superuser=0,
                is_staff=0,
                password=passwordOne,
                last_login=lastLogin,
                date_joined=dateJoined,
                is_active=1,
            )
            user.save()
            return redirect("login")
        else:
            message = 'Password didnot matched!'
            messages.warning(request, message)
            return render(request, self.template_name)


class LogoutView(DashboardView):
    def get(self, request):
        auth.logout(request)
        return redirect("login")


class UserView(View):
    template_name = "users/adminUserList.html"

    def get(self, request):
        allAuthUser = AuthUser.objects.all()
        context = {
            'allAuthUser': allAuthUser
        }
        return render(request, self.template_name, context)

    @csrf_exempt
    def post(self, request):
        id = request.POST.get('id')
        roleInfo = AuthUser.objects.filter(id=id).values()
        return JsonResponse({'roleInfo': list(roleInfo)})


def loginPage(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect("login")


def logout(request):
    auth.logout(request)
    return redirect("login")


def userList(request):
    allAuthUser = AuthUser.objects.all()
    context = {
        'allAuthUser': allAuthUser
    }
    return render(request, 'adminUserList.html', context)
