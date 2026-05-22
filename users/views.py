from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from team_finder.services import paginate
from users.forms import (
    LoginForm,
    ProfileEditForm,
    RegistrationForm,
    UserPasswordChangeForm,
)
from users.models import User
from users.services import get_filtered_users


def register(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("users:login")
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("projects:project_list")
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.user)
        return redirect("projects:project_list")
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("projects:project_list")


def user_detail(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    return render(request, "users/user-details.html", {"user": profile_user})


def user_list(request):
    participants, active_filter = get_filtered_users(request)
    page = paginate(participants, request)
    query_suffix = f"&filter={active_filter}" if active_filter else ""
    return render(
        request,
        "users/participants.html",
        {
            "participants": page,
            "page_obj": page,
            "active_filter": active_filter,
            "query_suffix": query_suffix,
        },
    )


@login_required
def edit_profile(request):
    form = ProfileEditForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    if form.is_valid():
        form.save()
        return redirect("users:user_detail", pk=request.user.pk)
    return render(
        request,
        "users/edit_profile.html",
        {"form": form, "user": request.user},
    )


@login_required
def change_password(request):
    form = UserPasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("users:user_detail", pk=request.user.pk)
    return render(request, "users/change_password.html", {"form": form})
