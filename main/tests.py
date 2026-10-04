import datetime
import uuid

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from main.models import Achievement, Experience, Project

TA = "Teaching Assistant · Programming Foundation 1 (DDP1)"
COMPFEST = "CTF Staff · COMPFEST 18"
NETSOS = "Member · NetSOS SIG"
POLRI = "1st place · POLRI CTF 2026"
FINDIT = "Finalist · FindIT! 2026 CTF"


class SeededDataTest(TestCase):
    def test_seeded_rows_and_ordering(self):
        self.assertEqual(Experience.objects.count(), 3)
        self.assertEqual(Achievement.objects.count(), 3)
        self.assertEqual(Project.objects.count(), 2)

        self.assertEqual([e.title for e in Experience.objects.all()], [TA, COMPFEST, NETSOS])
        titles = [a.title for a in Achievement.objects.all()]
        self.assertEqual(titles[0], POLRI)
        self.assertEqual(titles[-1], FINDIT)
        self.assertEqual(
            [p.name for p in Project.objects.all()],
            ["pwninit.py-demtcsre", "S4DFarm-demtcsre"],
        )
        self.assertEqual(
            [value for value, _ in Experience.EXPERIENCE_CHOICES],
            [
                "full-time",
                "part-time",
                "self-employed",
                "freelance",
                "contract",
                "internship",
                "apprenticeship",
                "seasonal",
            ],
        )

    def test_experience_str_category_and_ongoing_flag(self):
        experience = Experience.objects.get(title=TA)

        self.assertEqual(str(experience), TA)
        self.assertEqual(experience.category, "contract")
        self.assertEqual(experience.get_category_display(), "Contract")
        self.assertTrue(experience.is_ongoing)

        experience.ended_at = datetime.date(2026, 12, 1)
        experience.save()
        self.assertFalse(experience.is_ongoing)


class MainPageTest(TestCase):
    def setUp(self):
        self.url = reverse("main:show_main")

    def test_main_page_renders_every_section(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertTemplateUsed(response, "base.html")
        for section in ("profile", "experience", "achievement", "project"):
            self.assertContains(response, 'id="{}"'.format(section))
        for section in ("experience", "achievement", "project"):
            self.assertTemplateUsed(response, "sections/{}.html".format(section))
        for name in ("show_experience", "show_achievement", "show_project"):
            self.assertContains(response, 'href="{}"'.format(reverse("main:" + name)))
        self.assertContains(response, TA)
        self.assertContains(response, POLRI)
        self.assertContains(response, "pwninit.py-demtcsre")
        self.assertNotContains(response, "Hardcoded until")
        self.assertEqual(response.content.decode().count(TA), 1)

        self.assertEqual(self.client.get("/halaman-yang-tidak-ada/").status_code, 404)

    def test_main_page_caps_lists_at_three_without_padding(self):
        Experience.objects.create(
            title="Peran Terbaru",
            organization="Fakultas Ilmu Komputer",
            description="Dibuat oleh test.",
            category="internship",
            started_at=datetime.date(2030, 1, 1),
        )
        Project.objects.filter(name="S4DFarm-demtcsre").delete()

        response = self.client.get(self.url)

        self.assertEqual(Experience.objects.count(), 4)
        self.assertEqual(len(response.context["experience_list"]), 3)
        self.assertContains(response, "Peran Terbaru")
        self.assertNotContains(response, NETSOS)
        self.assertEqual(len(response.context["project_list"]), 1)
        self.assertNotContains(response, "Belum ada data project.")


class ExperiencePageTest(TestCase):
    def setUp(self):
        self.url = reverse("main:show_experience")

    def test_experience_page_lists_every_row(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertTemplateUsed(response, "sections/experience.html")
        self.assertEqual(len(response.context["experience_list"]), 3)
        for experience in Experience.objects.all():
            self.assertContains(response, experience.title)
            self.assertContains(response, experience.description)
            self.assertContains(response, experience.organization)
        self.assertContains(response, "Contract")
        self.assertContains(response, "Seasonal")
        self.assertNotContains(response, "Volunteer")
        self.assertContains(response, 'data-start="2026-08"')
        self.assertNotContains(response, "data-end=")
        self.assertContains(response, 'href="{}#experience"'.format(reverse("main:show_main")))

        Experience.objects.filter(title=TA).update(ended_at=datetime.date(2026, 12, 1))
        self.assertContains(self.client.get(self.url), 'data-end="2026-12"')

        Experience.objects.all().delete()
        self.assertContains(self.client.get(self.url), "Belum ada data experience.")

    def test_search_filters_by_title(self):
        response = self.client.get(self.url, {"title": "compfest"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual([e.title for e in response.context["experience_list"]], [COMPFEST])
        self.assertNotContains(response, NETSOS)
        self.assertContains(response, 'name="title" value="compfest"')

        response = self.client.get(reverse("main:get_experience_json"), {"title": "compfest"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["fields"]["title"] for item in response.json()], [COMPFEST])


class AchievementPageTest(TestCase):
    def setUp(self):
        self.url = reverse("main:show_achievement")

    def test_achievement_page_is_an_ajax_skeleton(self):
        response = self.client.get(self.url, {"title": "polri"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievement.html")
        self.assertTemplateUsed(response, "sections/achievement.html")
        self.assertNotIn("achievement_list", response.context)
        self.assertNotContains(response, POLRI)
        self.assertNotContains(response, FINDIT)
        for element_id in ("loading", "error", "empty", "grid", "achievement-search-form", "search-input"):
            self.assertContains(response, 'id="{}"'.format(element_id))
        self.assertContains(response, reverse("main:get_achievement_json"))
        self.assertEqual(response.context["title_query"], "polri")
        self.assertContains(response, 'value="polri"')
        self.assertContains(response, 'href="{}#achievement"'.format(reverse("main:show_main")))
        self.assertContains(response, "${escapeHtml(achievement.title)}")
        self.assertContains(response, "${escapeHtml(achievement.organizer)}")
        self.assertContains(response, "${escapeHtml(achievement.certificate)}")
        self.assertContains(response, 'const CAN_EDIT = "false"')
        self.assertContains(response, "const SEARCH_DEBOUNCE_DELAY = 300;")
        self.assertContains(response, 'searchInput.addEventListener("input"')

    def test_update_button_follows_change_achievement_perm(self):
        editor = User.objects.create_user("editor", password="pw")
        editor.user_permissions.add(Permission.objects.get(codename="change_achievement"))
        self.client.force_login(editor)

        self.assertContains(self.client.get(self.url), 'const CAN_EDIT = "true"')


class AchievementJsonTest(TestCase):
    def setUp(self):
        self.url = reverse("main:get_achievement_json")
        self.achievement = Achievement.objects.get(title=POLRI)
        self.other = Achievement.objects.get(title=FINDIT)

    def fields(self, achievement):
        return next(item["fields"] for item in self.client.get(self.url).json() if item["pk"] == str(achievement.id))

    def test_json_lists_filters_and_orders_achievements(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(
            [item["fields"]["title"] for item in response.json()],
            [a.title for a in Achievement.objects.all()],
        )
        self.assertTrue({"Aug 2026", "May 2026"} <= {item["fields"]["awarded_at"] for item in response.json()})
        self.assertEqual(self.fields(self.achievement)["certificate"], self.achievement.certificate)
        self.assertEqual(
            [item["fields"]["title"] for item in self.client.get(self.url, {"title": "polri"}).json()],
            [POLRI],
        )

    def test_star_fields_follow_the_viewer_and_the_toggle(self):
        self.achievement.starred_by.add(User.objects.create_user("a", password="pw"))

        fields = self.fields(self.achievement)
        self.assertEqual(fields["star_count"], 1)
        self.assertEqual(fields["starred_by_names"], "a")
        self.assertFalse(fields["is_starred"])

        self.client.force_login(User.objects.create_user("fan", password="pw"))
        star_url = reverse("main:toggle_achievement_star", args=[self.achievement.id])

        self.client.post(star_url)
        self.assertTrue(self.fields(self.achievement)["is_starred"])
        self.assertFalse(self.fields(self.other)["is_starred"])

        self.client.post(star_url)
        self.assertFalse(self.fields(self.achievement)["is_starred"])


class ProjectPageTest(TestCase):
    def setUp(self):
        self.url = reverse("main:show_project")

    def test_project_page_is_an_ajax_skeleton(self):
        response = self.client.get(self.url, {"name": "pwninit"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project.html")
        self.assertTemplateUsed(response, "sections/project.html")
        self.assertNotIn("project_list", response.context)
        self.assertNotContains(response, "pwninit.py-demtcsre")
        self.assertNotContains(response, "S4DFarm-demtcsre")
        for element_id in ("loading", "error", "empty", "grid", "project-search-form", "search-input"):
            self.assertContains(response, 'id="{}"'.format(element_id))
        self.assertContains(response, reverse("main:get_project_json"))
        self.assertContains(response, '<form id="project-search-form" class="project-search">')
        self.assertEqual(response.context["name_query"], "pwninit")
        self.assertContains(response, 'value="pwninit"')
        self.assertContains(response, 'href="{}#project"'.format(reverse("main:show_main")))
        self.assertContains(response, '<script src="/static/js/utils.js"></script>')
        self.assertContains(response, "${escapeHtml(project.name)}")
        self.assertContains(response, "${escapeHtml(project.description)}")
        self.assertNotContains(response, 'id="add-project-modal"')
        self.assertNotContains(response, 'popovertarget="add-project-modal"')

    def test_add_modal_is_only_for_superuser(self):
        self.client.force_login(User.objects.create_user("biasa", password="pw"))
        self.assertNotContains(self.client.get(self.url), 'id="add-project-modal"')

        self.client.force_login(User.objects.create_superuser("owner", password="pw"))
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "components/project_form_modal.html")
        self.assertContains(response, 'popovertarget="add-project-modal"')
        self.assertContains(response, '<form id="project-form"')
        self.assertContains(response, reverse("main:create_project_ajax"))
        for field in ("name", "kicker", "url", "description", "order"):
            self.assertContains(response, 'name="{}"'.format(field))


class ProjectJsonTest(TestCase):
    def setUp(self):
        self.url = reverse("main:get_project_json")
        self.project = Project.objects.get(name="pwninit.py-demtcsre")
        self.other = Project.objects.get(name="S4DFarm-demtcsre")

    def fields(self, project):
        return next(item["fields"] for item in self.client.get(self.url).json() if item["pk"] == str(project.id))

    def test_json_lists_filters_and_orders_projects(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(
            [item["fields"]["name"] for item in response.json()],
            ["pwninit.py-demtcsre", "S4DFarm-demtcsre"],
        )
        self.assertIn('<a href="https://github.com/sasha-999/pwninit.py">', self.fields(self.project)["description"])
        self.assertEqual(
            [item["fields"]["name"] for item in self.client.get(self.url, {"name": "s4dfarm"}).json()],
            ["S4DFarm-demtcsre"],
        )

    def test_star_fields_follow_the_viewer_and_the_toggle(self):
        self.project.starred_by.add(User.objects.create_user("a", password="pw"))

        fields = self.fields(self.project)
        self.assertEqual(fields["star_count"], 1)
        self.assertEqual(fields["starred_by_names"], "a")
        self.assertFalse(fields["is_starred"])

        self.client.force_login(User.objects.create_user("fan", password="pw"))
        star_url = reverse("main:toggle_project_star", args=[self.project.id])

        self.client.post(star_url)
        self.assertTrue(self.fields(self.project)["is_starred"])
        self.assertFalse(self.fields(self.other)["is_starred"])

        self.client.post(star_url)
        self.assertFalse(self.fields(self.project)["is_starred"])


class ProjectAjaxCreateTest(TestCase):
    def setUp(self):
        self.url = reverse("main:create_project_ajax")
        self.payload = {
            "name": "Proyek AJAX",
            "kicker": "Buatan test",
            "url": "https://example.com",
            "description": "Deskripsi.",
            "order": 3,
        }

    def test_only_superuser_with_csrf_can_post(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, 403)
        self.assertIn("message", response.json())

        self.client.force_login(User.objects.create_user("biasa", password="pw"))
        self.assertEqual(self.client.post(self.url, self.payload).status_code, 403)

        client = self.client_class(enforce_csrf_checks=True)
        client.force_login(User.objects.create_superuser("owner", password="pw"))
        self.assertEqual(client.post(self.url, self.payload).status_code, 403)

        self.assertEqual(Project.objects.count(), 2)

    def test_superuser_create_and_validation(self):
        self.client.force_login(User.objects.create_superuser("owner", password="pw"))

        self.assertEqual(self.client.get(self.url).status_code, 405)

        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, 201)
        project = Project.objects.get(pk=response.json()["pk"])
        self.assertEqual((project.name, project.kicker), ("Proyek AJAX", "Buatan test"))

        response = self.client.post(self.url, self.payload | {"name": "   "})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["errors"]["name"][0]["code"], "required")

        response = self.client.post(self.url, self.payload | {"url": "javascript:alert(1)"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("url", response.json()["errors"])

        response = self.client.post(self.url, self.payload | {"name": """<img src="x" onerror="alert('XSS!')">"""})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["errors"]["name"][0]["message"],
            "Nama proyek tidak boleh hanya berisi tag HTML.",
        )
        self.assertEqual(Project.objects.count(), 3)

        response = self.client.post(
            self.url,
            self.payload | {"name": "Halo <b>dunia</b>", "kicker": "<i>k</i>", "description": "<script>x</script>ok"},
        )
        project = Project.objects.get(pk=response.json()["pk"])
        self.assertEqual((project.name, project.kicker, project.description), ("Halo dunia", "k", "xok"))


class ProjectPermissionTest(TestCase):
    def setUp(self):
        self.project = Project.objects.first()

    def test_visitor_and_regular_user_are_blocked(self):
        response = self.client.get(reverse("main:create_project"))
        self.assertRedirects(
            response, "/login/?next=" + reverse("main:create_project"), fetch_redirect_response=False
        )

        user = User.objects.create_user("biasa", password="pw")
        self.client.force_login(user)
        update_url = reverse("main:update_project", args=[self.project.id])

        self.assertEqual(self.client.get(reverse("main:create_project")).status_code, 403)
        self.assertEqual(self.client.post(reverse("main:delete_project", args=[self.project.id])).status_code, 403)
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())
        self.assertEqual(self.client.get(update_url).status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename="change_project"))
        self.client.force_login(User.objects.get(pk=user.pk))
        self.assertEqual(self.client.get(update_url).status_code, 200)

    def test_superuser_can_add_and_delete(self):
        self.client.force_login(User.objects.create_superuser("owner", password="pw"))

        response = self.client.post(
            reverse("main:create_project"),
            {"name": "Proyek Baru", "kicker": "k", "url": "", "description": "d", "order": 3},
        )
        self.assertRedirects(response, reverse("main:show_project"))
        self.assertTrue(Project.objects.filter(name="Proyek Baru").exists())

        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))
        self.assertRedirects(response, reverse("main:show_project"))
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

        self.assertEqual(self.client.post(reverse("main:delete_project", args=[uuid.uuid4()])).status_code, 404)


class AchievementExperiencePermissionTest(TestCase):
    def test_only_superuser_can_create_and_delete(self):
        rows = {"achievement": Achievement.objects.first(), "experience": Experience.objects.first()}

        self.client.force_login(User.objects.create_user("biasa", password="pw"))
        for name, row in rows.items():
            self.assertEqual(self.client.get(reverse("main:create_" + name)).status_code, 403)
            self.assertEqual(self.client.post(reverse("main:delete_" + name, args=[row.id])).status_code, 403)
            self.assertTrue(type(row).objects.filter(pk=row.id).exists())

        self.client.force_login(User.objects.create_superuser("owner", password="pw"))
        for name, row in rows.items():
            self.assertEqual(self.client.get(reverse("main:create_" + name)).status_code, 200)
            self.client.post(reverse("main:delete_" + name, args=[row.id]))
            self.assertFalse(type(row).objects.filter(pk=row.id).exists())
