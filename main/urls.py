from django.urls import path

from main.views import (
    show_main,

    register,
    login_user,
    logout_user,

    show_project,
    create_project,
    create_project_ajax,
    update_project,
    delete_project,
    toggle_project_star,
    get_project_json,
    
    show_achievement,
    create_achievement,
    create_achievement_ajax,
    update_achievement,
    delete_achievement,
    toggle_achievement_star,
    get_achievement_json,
    
    show_experience,
    create_experience,
    create_experience_ajax,
    update_experience,
    delete_experience,
    get_experience_json,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),

    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/add-ajax/", create_experience_ajax, name="create_experience_ajax"),
    path('experience/<uuid:experience_id>/update/', update_experience, name='update_experience'),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),

    path("achievement/", show_achievement, name="show_achievement"),
    path("achievement/add/", create_achievement, name="create_achievement"),
    path("achievement/add-ajax/", create_achievement_ajax, name="create_achievement_ajax"),
    path('achievement/<uuid:achievement_id>/update/', update_achievement, name='update_achievement'),
    path("achievement/<uuid:achievement_id>/delete/", delete_achievement, name="delete_achievement"),
    path("achievement/<uuid:achievement_id>/star/", toggle_achievement_star, name="toggle_achievement_star"),
    path("api/achievement/", get_achievement_json, name="get_achievement_json"),

    path("project/", show_project, name="show_project"),
    path("project/add/", create_project, name="create_project"),
    path("project/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path('project/<uuid:project_id>/update/', update_project, name='update_project'),
    path("project/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("project/<uuid:project_id>/star/", toggle_project_star, name="toggle_project_star"),
    path("api/project/", get_project_json, name="get_project_json"),
]
