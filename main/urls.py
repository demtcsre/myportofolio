from django.urls import path

from main.views import (
    show_project,
    create_project,
    update_project,
    delete_project,
    get_project_json,
    show_achievement,
    create_achievement,
    update_achievement,
    delete_achievement,
    get_achievement_json,
    show_experience,
    create_experience,
    update_experience,
    delete_experience,
    get_experience_json,
    show_main,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path('experience/<uuid:experience_id>/update/', update_experience, name='update_experience'),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("achievement/", show_achievement, name="show_achievement"),
    path("achievement/add/", create_achievement, name="create_achievement"),
    path('achievement/<uuid:achievement_id>/update/', update_achievement, name='update_achievement'),
    path("achievement/<uuid:achievement_id>/delete/", delete_achievement, name="delete_achievement"),
    path("api/achievement/", get_achievement_json, name="get_projeget_achievement_jsonct_json"),
    path("project/", show_project, name="show_project"),
    path("project/add/", create_project, name="create_project"),
    path('project/<uuid:project_id>/update/', update_project, name='update_project'),
    path("project/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("api/project/", get_project_json, name="get_project_json"),
]
