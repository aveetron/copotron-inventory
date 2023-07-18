from datetime import datetime

from django.contrib import auth, messages
from django.contrib.auth import login as auth_login
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from item.views import DashboardView
from users.models import AuthUser


class LoginView(View):
    """
        pipeline test t2
    """
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
                    messages.warning(request, "No user found!")
                    return redirect("login")
            else:
                messages.warning(request, "email or password is missing!")
                return redirect("login")
        except Exception as e:
            messages.warning(request, e.args[0])
            return redirect("login")


class RegistrationView(DashboardView):
    template_name = "users/registration.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
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
                messages.success(request, "Successfully registered, now login.")
                return redirect("login")
            else:
                message = "Password didnot matched!"
                messages.warning(request, message)
                return render(request, self.template_name)
        except Exception as e:
            messages.warning(request, e.args[0])
            return render(request, self.template_name)


class LogoutView(DashboardView):
    def get(self, request):
        auth.logout(request)
        return redirect("login")


class UserView(View):
    template_name = "users/adminUserList.html"

    def get(self, request):
        allAuthUser = AuthUser.objects.all()
        context = {"allAuthUser": allAuthUser}
        return render(request, self.template_name, context)

    @csrf_exempt
    def post(self, request):
        id = request.POST.get("id")
        roleInfo = AuthUser.objects.filter(id=id).values()
        return JsonResponse({"roleInfo": list(roleInfo)})


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
    context = {"allAuthUser": allAuthUser}
    return render(request, "adminUserList.html", context)
