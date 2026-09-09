from django.urls import path

from main.views import show_achievement, show_experience, show_main, show_project

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("achievement/", show_achievement, name="show_achievement"),
    path("project/", show_project, name="show_project"),
]
