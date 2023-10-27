from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render
from .forms import *


def index(request):
    return render(request, "Employe/index.html")


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, "Employe/login.html", {})


@login_required
def edit_profile(request):
    user_form = EmployeEditForm(instance=request.user)
    if request.user.is_authenticated():
        if request.method == "POST":
            user_form = EmployeEditForm(
                request.POST, request.FILES, instance=request.user
            )
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                created_user.save()
                return HttpResponseRedirect("/")

        return render(
            request,
            "Employe/edit.html",
            {
                "form": user_form,
            },
        )
    else:
        raise PermissionDenied


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return HttpResponseRedirect("/")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "Employe/changePassword.html", {"form": form})
