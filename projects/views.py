from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from projects.forms import ProjectForm
from projects.models import Project


def _favorite_ids(user):
    if not user.is_authenticated:
        return set()
    return set(user.favorites.values_list("pk", flat=True))


def project_list(request):
    queryset = Project.objects.select_related("owner").prefetch_related("participants")
    paginator = Paginator(queryset, 12)
    page = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "projects/project_list.html",
        {
            "projects": page,
            "page_obj": page,
            "favorite_ids": _favorite_ids(request.user),
        },
    )


@login_required
def favorite_projects(request):
    queryset = (
        request.user.favorites.select_related("owner")
        .prefetch_related("participants")
        .order_by("-created_at")
    )
    paginator = Paginator(queryset, 12)
    page = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "projects/favorite_projects.html",
        {
            "projects": page,
            "page_obj": page,
            "favorite_ids": _favorite_ids(request.user),
        },
    )


def project_detail(request, pk):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("participants"),
        pk=pk,
    )
    return render(
        request,
        "projects/project-details.html",
        {
            "project": project,
            "favorite_ids": _favorite_ids(request.user),
        },
    )


@login_required
@require_POST
def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)
    favorites = request.user.favorites
    if favorites.filter(pk=project.pk).exists():
        favorites.remove(project)
        favorited = False
    else:
        favorites.add(project)
        favorited = True
    return JsonResponse({"status": "ok", "favorited": favorited})


@login_required
@require_POST
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner_id == request.user.id:
        return JsonResponse({"status": "error"}, status=403)
    participants = project.participants
    if participants.filter(pk=request.user.pk).exists():
        participants.remove(request.user)
        return JsonResponse({"status": "ok", "participant": False})
    participants.add(request.user)
    return JsonResponse({"status": "ok", "participant": True})


@login_required
@require_POST
def complete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner_id != request.user.id or project.status != Project.STATUS_OPEN:
        return JsonResponse({"status": "error"}, status=403)
    project.status = Project.STATUS_CLOSED
    project.save(update_fields=["status"])
    return JsonResponse({"status": "ok", "project_status": "closed"})


@login_required
def create_project(request):
    return _project_form(request, project=None, is_edit=False)


@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    return _project_form(request, project=project, is_edit=True)


def _project_form(request, project, is_edit):
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            saved = form.save(commit=False)
            if not is_edit:
                saved.owner = request.user
            saved.save()
            if not is_edit:
                saved.participants.add(request.user)
            return redirect("projects:project_detail", pk=saved.pk)
    else:
        form = ProjectForm(instance=project)
    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": is_edit},
    )
