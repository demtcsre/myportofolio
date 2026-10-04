import datetime

from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required 
from django.core import serializers
from django.core.exceptions import PermissionDenied 
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

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
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    return HttpResponse(serializers.serialize("json", experiences, use_natural_foreign_keys=True), content_type="application/json")

def show_experience(request):
    payload = get_experience_json(request).content.decode("utf-8")
    experience_list = [experience.object for experience in serializers.deserialize("json", payload)]

    context = PROFILE | {
        "experience_list": experience_list,
        "title_query": request.GET.get("title", "").strip(),
    }
    return render(request, "experience.html", context)

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience successfully added!")
        return redirect("main:show_experience")

    return render(request, "forms/experiences_form.html", PROFILE | {"form": form})

@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not request.user.has_perm("main.change_experience"):
        raise PermissionDenied
    
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
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        get_object_or_404(Experience, pk=experience_id).delete()
        messages.success(request, "Experience successfully deleted!")

    return redirect("main:show_experience")

def get_achievement_json(request):
    title_query = request.GET.get("title", "").strip()
    achievements = Achievement.objects.prefetch_related('starred_by').all()

    if title_query:
        achievements = achievements.filter(title__icontains=title_query)

    data = []
    for achievement in achievements:
        starred_users = achievement.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(achievement.id),
            "fields": {
                "title": achievement.title,
                "organizer": achievement.organizer,
                "awarded_at": achievement.awarded_at.strftime("%b %Y"),
                "certificate": achievement.certificate,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

def show_achievement(request):
    title_query = request.GET.get("title", "").strip()
    achievement_list = Achievement.objects.all()

    if title_query:
        achievement_list = achievement_list.filter(title__icontains=title_query)

    context = PROFILE | {
        "achievement_list": achievement_list,
        "title_query": title_query,
    }
    return render(request, "achievement.html", context)

@login_required(login_url="/login/")
def create_achievement(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = AchievementForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New achievement successfully added!")
        return redirect("main:show_achievement")

    return render(request, "forms/achievements_form.html", PROFILE | {"form": form})

@login_required(login_url="/login/")
def update_achievement(request, achievement_id):
    if not request.user.has_perm("main.change_achievement"):
        raise PermissionDenied
    
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
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        get_object_or_404(Achievement, pk=achievement_id).delete()
        messages.success(request, "Achievement successfully deleted!")

    return redirect("main:show_achievement")

@login_required(login_url="/login/")
def toggle_achievement_star(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)

    if request.method == "POST":
        if request.user in achievement.starred_by.all():
            achievement.starred_by.remove(request.user)
        else:
            achievement.starred_by.add(request.user)

    return redirect("main:show_achievement")

def get_project_json(request):
    name_query = request.GET.get("name", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if name_query:
        projects = projects.filter(name__icontains=name_query)

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "name": project.name,
                "kicker": project.kicker,
                "url": project.url,
                "description": project.description,
                "order": project.order,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

def show_project(request):
    context = PROFILE | {
        "name_query": request.GET.get("name", "").strip(),
        "form": ProjectForm(),
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

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@login_required(login_url="/login/")
def update_project(request, project_id):
    if not request.user.has_perm("main.change_project"):
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