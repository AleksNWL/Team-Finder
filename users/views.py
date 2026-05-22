from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from users.forms import (
    LoginForm,
    ProfileEditForm,
    RegistrationForm,
    UserPasswordChangeForm,
)
from users.models import User


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
        return render(request, "users/register.html", {"form": form})
    return render(request, "users/register.html", {"form": RegistrationForm()})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("projects:project_list")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("projects:project_list")
        return render(request, "users/login.html", {"form": form})
    return render(request, "users/login.html", {"form": LoginForm()})


def logout_view(request):
    logout(request)
    return redirect("projects:project_list")


def user_detail(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    return render(request, "users/user-details.html", {"user": profile_user})


def _filtered_users(request):
    queryset = User.objects.order_by("-date_joined")
    active_filter = request.GET.get("filter")
    if not request.user.is_authenticated or not active_filter:
        return queryset, active_filter

    user = request.user
    if active_filter == "owners-of-favorite-projects":
        queryset = queryset.filter(owned_projects__in=user.favorites.all())
    elif active_filter == "owners-of-participating-projects":
        queryset = queryset.filter(
            owned_projects__participants=user,
        ).exclude(pk=user.pk)
    elif active_filter == "interested-in-my-projects":
        queryset = queryset.filter(favorites__owner=user)
    elif active_filter == "participants-of-my-projects":
        queryset = queryset.filter(
            participated_projects__owner=user,
        ).exclude(pk=user.pk)
    else:
        active_filter = None
    return queryset.distinct(), active_filter


def user_list(request):
    participants, active_filter = _filtered_users(request)
    paginator = Paginator(participants, 12)
    page = paginator.get_page(request.GET.get("page"))
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
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:user_detail", pk=request.user.pk)
        return render(
            request,
            "users/edit_profile.html",
            {"form": form, "user": request.user},
        )
    form = ProfileEditForm(instance=request.user)
    return render(
        request,
        "users/edit_profile.html",
        {"form": form, "user": request.user},
    )


@login_required
def change_password(request):
    if request.method == "POST":
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:user_detail", pk=request.user.pk)
        return render(request, "users/change_password.html", {"form": form})
    return render(
        request,
        "users/change_password.html",
        {"form": UserPasswordChangeForm(request.user)},
    )
