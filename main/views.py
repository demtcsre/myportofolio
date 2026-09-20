import secrets
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView


from main.models import Achievement, Experience, Project
from main.forms import ProjectForm

PROFILE = {
    "name": "Ahmad Rizki Daffaa",
    "npm": "2506543640",
    "study_program": "S1 Ilmu Komputer",
    "bio": "Second-year CS student at Universitas Indonesia, passionate in Cybersecurity and Data Science while also being a teaching assistant in Programming Foundation 1 (DDP1) course.",
}

def require_secret(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        code = settings.SECRET_CODE
        if request.method == "POST" and not (
            code and secrets.compare_digest(request.POST.get("secret_code", ""), code)
        ):
            messages.error(request, "Wrong or missing secret code.")
            return redirect(request.path)
        return view(request, *args, **kwargs)

    return wrapper


def show_main(request):
    context = PROFILE | {
        "experience_list": Experience.objects.all()[:3],
        "achievement_list": Achievement.objects.all()[:3],
        "project_list": Project.objects.all()[:3],
    }
    return render(request, "index.html", context)


def show_experience(request):
    return render(request, "experience.html", PROFILE | {"experience_list": Experience.objects.all()})


def show_achievement(request):
    return render(request, "achievement.html", PROFILE | {"achievement_list": Achievement.objects.all()})


def get_project_json(request):
    name_query = request.GET.get("name", "").strip()
    projects = Project.objects.all()

    if name_query:
        projects = projects.filter(name__icontains=name_query)

    return HttpResponse(serializers.serialize("json", projects), content_type="application/json")


def show_project(request):
    payload = get_project_json(request).content.decode("utf-8")
    project_list = [project.object for project in serializers.deserialize("json", payload)]

    context = PROFILE | {
        "project_list": project_list,
        "name_query": request.GET.get("name", "").strip(),
    }
    return render(request, "project.html", context)


@require_secret
def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New project successfully added!")
        return redirect("main:show_project")

    return render(request, "forms/projects_form.html", PROFILE | {"form": form})

@require_secret
def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project successfully updated!")
            return redirect("main:show_project")
    else:
        form = ProjectForm(instance=project)

    context = PROFILE | {
        "form": form,
        "is_update": True,
        "project": project
    }
    return render(request, "forms/projects_form.html", context)

@require_secret
def delete_project(request, project_id):
    if request.method == "POST":
        get_object_or_404(Project, pk=project_id).delete()
        messages.success(request, "Project successfully deleted!")

    return redirect("main:show_project")
