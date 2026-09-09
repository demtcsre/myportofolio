from django.shortcuts import render

from main.models import Achievement, Experience, Project

PROFILE = {
    "name": "Ahmad Rizki Daffaa",
    "npm": "2506543640",
    "study_program": "S1 Ilmu Komputer",
    "bio": "Second-year CS student at Universitas Indonesia, passionate in Cybersecurity and Data Science while also being a teaching assistant in Programming Foundation 1 (DDP1) course.",
}


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


def show_project(request):
    return render(request, "project.html", PROFILE | {"project_list": Project.objects.all()})
