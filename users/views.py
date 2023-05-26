from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from .models import *
import datetime
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib import auth
from django.contrib import messages
from item.views import DashboardView

from django.views.generic import View
from django.db.models import Sum
from django.views.decorators.csrf import *
from django.http import JsonResponse

# Create your views here.


class LoginView(DashboardView,):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            if request.method == "POST":
                username = request.POST.get("username")
                password = request.POST.get("password")
                if username and password:
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        auth_login(request, user)
                        user.save()
                        print("logged in successfully")
                        message = "you are successfully logged in"
                        messages.success(request, message)
                        return redirect("dashboard")
                    else:
                        print("wrong username and password")
                        return redirect("login")
                else:
                    print("login failed")
                    return redirect("login")
        except:
            message = "login failed"
            messages.warning(request, message)
            return redirect("login")


class RegistrationView(DashboardView):
    template_name = "registration.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        email = request.POST.get("email")
        passwordOne = request.POST.get("passwordOne")
        passwordTwo = request.POST.get("passwordTwo")
        username = firstName+lastName
        lastLogin = datetime.now()
        dateJoined = datetime.now()
        if passwordOne == passwordTwo:
            User.objects.create_user(
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
            return redirect("login")
        else:
            print('password didnot matched')
            message = 'User alrady exists'
            messages.warning(request, message)
            return render(request, 'registration.html')


class LogoutView(DashboardView):
    def get(self, request):
        auth.logout(request)
        return redirect("login")


class UserView(View):
    template_name = "adminUserList.html"

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


class RolePermissionUpdateView(View):
    def post(self, request):
        try:
            getRoleInfo = AuthUser.objects.get(id=request.POST.get('id'))
            getRoleInfo.is_active = request.POST.get('employeeStatus')
            getRoleInfo.is_staff = request.POST.get('staffStatus')
            getRoleInfo.is_superuser = int(request.POST.get('adminStatus'))
            getRoleInfo.save()
            message = 'User Role Updated'
            messages.success(request, message)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except:
            message = 'User permission change cannot be applied!'
            messages.warning(request, message)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def registration(request):
    if request.method == "POST":
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        email = request.POST.get("email")
        passwordOne = request.POST.get("passwordOne")
        passwordTwo = request.POST.get("passwordTwo")
        lastLogin = datetime.now()
        dateJoined = datetime.now()
        if passwordOne == passwordTwo:
            User.objects.create_user(
                username=firstName + lastName,
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
            return redirect("login")
        else:
            print('password didnot matched')
            message = 'User alrady exists'
            messages.warning(request, message)
            return render(request, 'registration.html')
    else:
        print("else block")
        return render(request, "registration.html")


def loginPage(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    else:
        return redirect("login")


def login(request):
    return render(request, "login.html")


def loginCheck(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                user.save()
                print("logged in successfully")
                message = "you are successfully logged in"
                messages.success(request, message)
                return redirect("home")
            else:
                print("wrong username and password")
                return redirect("login")
        else:
            print("login failed")
            return redirect("login")
    else:
        print("login problem")
        return redirect("login")


@login_required(login_url="loginPage")
def home(request):
    if request.user.is_superuser is True or request.user.is_staff is True:
        totalCustomer = AuthUser.objects.all().count()
        return redirect("dashboard")
    else:
        return redirect("login")


def logout(request):
    auth.logout(request)
    return redirect("login")


@login_required(login_url='loginPage')
def userList(request):
    allAuthUser = AuthUser.objects.all()
    context = {
        'allAuthUser': allAuthUser
    }
    return render(request, 'adminUserList.html', context)


@csrf_exempt
def rolePermissionView(request):
    id = request.POST.get('id')
    roleInfo = AuthUser.objects.filter(id=id).values()
    return JsonResponse({'roleInfo': list(roleInfo)})


@login_required(login_url='loginPage')
def rolePermissionUpdate(request):
    try:
        getRoleInfo = AuthUser.objects.get(id=request.POST.get('id'))
        getRoleInfo.is_active = request.POST.get('employeeStatus')
        getRoleInfo.is_staff = request.POST.get('staffStatus')
        getRoleInfo.is_superuser = int(request.POST.get('adminStatus'))
        getRoleInfo.save()
        message = 'User Role Updated'
        messages.success(request, message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        message = 'User permission change cannot be applied!'
        messages.warning(request, message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
