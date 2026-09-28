import datetime

from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required 
from django.core import serializers
from django.core.exceptions import PermissionDenied 
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

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Ahmad Rizki Daffaa",
        "form": form,
    }
    return render(request, "auth/register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Ahmad Rizki Daffaa",
        "form": form,
    }
    return render(request, "auth/login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = PROFILE | {
        "experience_list": Experience.objects.all()[:3],
        "achievement_list": Achievement.objects.all()[:3],
        "project_list": Project.objects.all()[:3],
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def get_experience_json(request):
    name_query = request.GET.get("name", "").strip()
    experiences = Experience.objects.all()

    if name_query:
        experiences = experiences.filter(name__icontains=name_query)

    return HttpResponse(serializers.serialize("json", experiences, use_natural_foreign_keys=True), content_type="application/json")


def show_experience(request):
    payload = get_experience_json(request).content.decode("utf-8")
    experience_list = [experience.object for experience in serializers.deserialize("json", payload)]

    context = PROFILE | {
        "experience_list": experience_list,
        "name_query": request.GET.get("name", "").strip(),
    }
    return render(request, "experience.html", context)


@login_required(login_url="/login/")
def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience successfully added!")
        return redirect("main:show_experience")

    return render(request, "forms/experiences_form.html", PROFILE | {"form": form})

@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
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

    return HttpResponse(serializers.serialize("json", achievements, use_natural_foreign_keys=True), content_type="application/json")


def show_achievement(request):
    payload = get_achievement_json(request).content.decode("utf-8")
    achievement_list = [achievement.object for achievement in serializers.deserialize("json", payload)]

    context = PROFILE | {
        "achievement_list": achievement_list,
        "name_query": request.GET.get("name", "").strip(),
    }
    return render(request, "achievement.html", context)


@login_required(login_url="/login/")
def create_achievement(request):
    form = AchievementForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New achievement successfully added!")
        return redirect("main:show_achievement")

    return render(request, "forms/achievements_form.html", PROFILE | {"form": form})

@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
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

    return HttpResponse(serializers.serialize("json", projects, use_natural_foreign_keys=True), content_type="application/json")


def show_project(request):
    payload = get_project_json(request).content.decode("utf-8")
    project_list = [project.object for project in serializers.deserialize("json", payload)]

    context = PROFILE | {
        "project_list": project_list,
        "name_query": request.GET.get("name", "").strip(),
    }
    return render(request, "project.html", context)


@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New project successfully added!")
        return redirect("main:show_project")

    return render(request, "forms/projects_form.html", PROFILE | {"form": form})

@login_required(login_url="/login/")
def update_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == "POST":
        get_object_or_404(Project, pk=project_id).delete()
        messages.success(request, "Project successfully deleted!")

    return redirect("main:show_project")

@login_required(login_url="/login/")
def toggle_project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_project")