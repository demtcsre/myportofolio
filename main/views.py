import secrets
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Achievement, Experience, Project
from main.forms import AchievementForm, ExperienceForm, ProjectForm

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


def get_experience_json(request):
    name_query = request.GET.get("name", "").strip()
    experiences = Experience.objects.all()

    if name_query:
        experiences = experiences.filter(name__icontains=name_query)

    return HttpResponse(serializers.serialize("json", experiences), content_type="application/json")


def show_experience(request):
    payload = get_experience_json(request).content.decode("utf-8")
    experience_list = [experience.object for experience in serializers.deserialize("json", payload)]

    context = PROFILE | {
        "experience_list": experience_list,
        "name_query": request.GET.get("name", "").strip(),
    }
    return render(request, "experience.html", context)


@require_secret
def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience successfully added!")
        return redirect("main:show_experience")

    return render(request, "forms/experiences_form.html", PROFILE | {"form": form})

@require_secret
def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    
    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, "Experience successfully updated!")
            return redirect("main:show_experience")
    else:
        form = ExperienceForm(instance=experience)

    context = PROFILE | {
        "form": form,
        "is_update": True,
        "experience": experience
    }
    return render(request, "forms/experiences_form.html", context)

@require_secret
def delete_experience(request, experience_id):
    if request.method == "POST":
        get_object_or_404(Experience, pk=experience_id).delete()
        messages.success(request, "Experience successfully deleted!")

    return redirect("main:show_experience")


def get_achievement_json(request):
    name_query = request.GET.get("name", "").strip()
    achievements = Achievement.objects.all()

    if name_query:
        achievements = achievements.filter(name__icontains=name_query)

    return HttpResponse(serializers.serialize("json", achievements), content_type="application/json")


def show_achievement(request):
    payload = get_achievement_json(request).content.decode("utf-8")
    achievement_list = [achievement.object for achievement in serializers.deserialize("json", payload)]

    context = PROFILE | {
        "achievement_list": achievement_list,
        "name_query": request.GET.get("name", "").strip(),
    }
    return render(request, "achievement.html", context)


@require_secret
def create_achievement(request):
    form = AchievementForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New achievement successfully added!")
        return redirect("main:show_achievement")

    return render(request, "forms/achievements_form.html", PROFILE | {"form": form})

@require_secret
def update_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    
    if request.method == "POST":
        form = AchievementForm(request.POST, instance=achievement)
        if form.is_valid():
            form.save()
            messages.success(request, "Achievement successfully updated!")
            return redirect("main:show_achievement")
    else:
        form = AchievementForm(instance=achievement)

    context = PROFILE | {
        "form": form,
        "is_update": True,
        "achievement": achievement
    }
    return render(request, "forms/achievements_form.html", context)

@require_secret
def delete_achievement(request, achievement_id):
    if request.method == "POST":
        get_object_or_404(Achievement, pk=achievement_id).delete()
        messages.success(request, "Achievement successfully deleted!")

    return redirect("main:show_achievement")


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
