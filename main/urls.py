from django.urls import path

from main.views import (
    create_project,
    delete_project,
    get_project_json,
    show_achievement,
    show_experience,
    show_main,
    show_project,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("achievement/", show_achievement, name="show_achievement"),
    path("project/", show_project, name="show_project"),
    path("project/add/", create_project, name="create_project"),
    path("project/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("api/project/", get_project_json, name="get_project_json"),
]
