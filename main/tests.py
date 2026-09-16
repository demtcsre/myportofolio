import datetime
import json
import uuid

from django.test import TestCase, override_settings
from django.urls import reverse

from main.models import Achievement, Experience, Project

TA = "Teaching Assistant · Programming Foundation 1 (DDP1)"
COMPFEST = "CTF Staff · COMPFEST 18"
NETSOS = "Member · NetSOS SIG"
POLRI = "1st place · POLRI CTF 2026"
FINDIT = "Finalist · FindIT! 2026 CTF"


class SeededDataTest(TestCase):
    def test_seed_migration_fills_every_model(self):
        self.assertEqual(Experience.objects.count(), 3)
        self.assertEqual(Achievement.objects.count(), 3)
        self.assertEqual(Project.objects.count(), 2)

    def test_experience_str_and_ongoing_flag(self):
        experience = Experience.objects.get(title=TA)

        self.assertEqual(str(experience), TA)
        self.assertEqual(experience.category, "contract")
        self.assertEqual(experience.get_category_display(), "Contract")
        self.assertTrue(experience.is_ongoing)

    def test_completed_experience_is_not_ongoing(self):
        experience = Experience.objects.get(title=TA)
        experience.ended_at = datetime.date(2026, 12, 1)
        experience.save()

        self.assertFalse(experience.is_ongoing)

    def test_experience_is_ordered_newest_first(self):
        self.assertEqual(
            [experience.title for experience in Experience.objects.all()],
            [TA, COMPFEST, NETSOS],
        )

    def test_achievement_breaks_a_date_tie_by_title(self):
        titles = [achievement.title for achievement in Achievement.objects.all()]

        self.assertEqual(titles[0], POLRI)
        self.assertEqual(titles[-1], FINDIT)

    def test_project_uses_its_explicit_order(self):
        self.assertEqual(
            [project.name for project in Project.objects.all()],
            ["pwninit.py-demtcsre", "S4DFarm-demtcsre"],
        )

    def test_category_choices_follow_linkedin(self):
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


class MainPageTest(TestCase):
    def setUp(self):
        self.url = reverse("main:show_main")

    def test_main_url_is_accessible(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertTemplateUsed(response, "base.html")

    def test_main_page_renders_all_four_sections(self):
        response = self.client.get(self.url)

        for section in ("profile", "experience", "achievement", "project"):
            self.assertContains(response, 'id="{}"'.format(section))

    def test_main_page_includes_each_section_partial(self):
        response = self.client.get(self.url)

        for section in ("experience", "achievement", "project"):
            self.assertTemplateUsed(response, "sections/{}.html".format(section))

    def test_main_page_links_to_every_section_page(self):
        response = self.client.get(self.url)

        for name in ("show_experience", "show_achievement", "show_project"):
            self.assertContains(response, 'href="{}"'.format(reverse("main:" + name)))

    def test_main_page_shows_content_from_all_three_models(self):
        response = self.client.get(self.url)

        self.assertContains(response, TA)
        self.assertContains(response, POLRI)
        self.assertContains(response, "pwninit.py-demtcsre")

    def test_main_page_shows_at_most_three_experiences(self):
        Experience.objects.create(
            title="Peran Terbaru",
            organization="Fakultas Ilmu Komputer",
            description="Dibuat oleh test.",
            category="internship",
            started_at=datetime.date(2030, 1, 1),
        )

        response = self.client.get(self.url)

        self.assertEqual(Experience.objects.count(), 4)
        self.assertEqual(len(response.context["experience_list"]), 3)
        self.assertContains(response, "Peran Terbaru")
        self.assertNotContains(response, NETSOS)

    def test_main_page_shows_fewer_than_three_without_padding(self):
        Project.objects.filter(name="S4DFarm-demtcsre").delete()

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["project_list"]), 1)
        self.assertNotContains(response, "Belum ada data project.")

    def test_commented_out_markup_never_reaches_the_browser(self):
        # index.html menyimpan markup lama di dalam tag comment Django, yang
        # dibuang sebelum respons dikirim. HTML comment biasa tetap terkirim.
        response = self.client.get(self.url)

        self.assertNotContains(response, "Hardcoded until")
        self.assertEqual(response.content.decode().count(TA), 1)

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)


class ExperiencePageTest(TestCase):
    def setUp(self):
        self.url = reverse("main:show_experience")

    def test_experience_page_is_accessible(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertTemplateUsed(response, "sections/experience.html")

    def test_experience_page_lists_every_row(self):
        response = self.client.get(self.url)

        self.assertEqual(len(response.context["experience_list"]), 3)
        for experience in Experience.objects.all():
            self.assertContains(response, experience.title)
            self.assertContains(response, experience.description)
            self.assertContains(response, experience.organization)

    def test_experience_page_shows_linkedin_category_labels(self):
        response = self.client.get(self.url)

        self.assertContains(response, "Contract")
        self.assertContains(response, "Seasonal")
        self.assertNotContains(response, "Volunteer")

    def test_ongoing_experience_emits_no_data_end(self):
        # script.js justru menulis "Present" ketika data-end tidak ada.
        response = self.client.get(self.url)

        self.assertContains(response, 'data-start="2026-08"')
        self.assertNotContains(response, "data-end=")

    def test_completed_experience_emits_data_end(self):
        experience = Experience.objects.get(title=TA)
        experience.ended_at = datetime.date(2026, 12, 1)
        experience.save()

        response = self.client.get(self.url)

        self.assertContains(response, 'data-end="2026-12"')

    def test_experience_page_links_back_to_main(self):
        response = self.client.get(self.url)

        self.assertContains(
            response, 'href="{}#experience"'.format(reverse("main:show_main"))
        )

    def test_empty_experience_page(self):
        Experience.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Belum ada data experience.")


class AchievementPageTest(TestCase):
    def setUp(self):
        self.url = reverse("main:show_achievement")

    def test_achievement_page_is_accessible(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievement.html")
        self.assertTemplateUsed(response, "sections/achievement.html")

    def test_achievement_page_lists_every_row(self):
        response = self.client.get(self.url)

        self.assertEqual(len(response.context["achievement_list"]), 3)
        for achievement in Achievement.objects.all():
            self.assertContains(response, achievement.title)
            self.assertContains(response, achievement.organizer)
            self.assertContains(response, achievement.certificate)

    def test_achievement_page_formats_the_award_date(self):
        response = self.client.get(self.url)

        self.assertContains(response, "Aug 2026")
        self.assertContains(response, "May 2026")

    def test_certificate_image_has_alt_text(self):
        response = self.client.get(self.url)

        self.assertContains(response, 'alt="Certificate:')

    def test_achievement_page_links_back_to_main(self):
        response = self.client.get(self.url)

        self.assertContains(
            response, 'href="{}#achievement"'.format(reverse("main:show_main"))
        )

    def test_empty_achievement_page(self):
        Achievement.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Belum ada data achievement.")


class ProjectPageTest(TestCase):
    def setUp(self):
        self.url = reverse("main:show_project")

    def test_project_page_is_accessible(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project.html")
        self.assertTemplateUsed(response, "sections/project.html")

    def test_project_page_lists_every_row(self):
        response = self.client.get(self.url)

        self.assertEqual(len(response.context["project_list"]), 2)
        for project in Project.objects.all():
            self.assertContains(response, project.name)
            self.assertContains(response, project.kicker)
            self.assertContains(response, project.url)

    def test_project_description_keeps_its_inline_links(self):
        # description dirender dengan |safe, jadi tag <a> di dalamnya harus utuh
        # dan bukan teks yang ter-escape.
        response = self.client.get(self.url)

        self.assertContains(response, '<a href="https://github.com/sasha-999/pwninit.py">')
        self.assertNotContains(response, "&lt;a href=")

    def test_project_page_keeps_the_explicit_order(self):
        body = self.client.get(self.url).content.decode()

        self.assertLess(body.index("pwninit.py-demtcsre"), body.index("S4DFarm-demtcsre"))

    def test_project_page_links_back_to_main(self):
        response = self.client.get(self.url)

        self.assertContains(
            response, 'href="{}#project"'.format(reverse("main:show_main"))
        )

    def test_empty_project_page(self):
        Project.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Belum ada data project.")


class ProjectJsonTest(TestCase):
    def setUp(self):
        self.url = reverse("main:get_project_json")

    def test_json_endpoint_serves_every_project(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_json_endpoint_filters_by_name(self):
        response = self.client.get(self.url, {"name": "s4dfarm"})
        payload = json.loads(response.content)

        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["fields"]["name"], "S4DFarm-demtcsre")

    def test_project_page_search_narrows_the_list(self):
        response = self.client.get(reverse("main:show_project"), {"name": "pwninit"})

        self.assertEqual(len(response.context["project_list"]), 1)
        self.assertEqual(response.context["name_query"], "pwninit")
        self.assertNotContains(response, "S4DFarm-demtcsre")


@override_settings(SECRET_CODE="kode-rahasia")
class SecretCodeGateTest(TestCase):
    """Add dan delete cuma boleh jalan kalau secret_code yang dikirim benar."""

    def setUp(self):
        self.add_url = reverse("main:create_project")
        self.payload = {
            "name": "Proyek Baru",
            "kicker": "Buatan test",
            "description": "Deskripsi.",
            "url": "https://example.com",
            "order": 3,
            "secret_code": "kode-rahasia",
        }

    def without_code(self, **overrides):
        payload = self.payload | overrides
        payload.pop("secret_code", None)
        return payload

    def test_add_form_page_stays_public(self):
        response = self.client.get(self.add_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forms/projects_form.html")

    def test_add_form_asks_for_the_code_without_leaking_it(self):
        response = self.client.get(self.add_url)

        self.assertContains(response, 'name="secret_code"')
        self.assertContains(response, 'type="password"')
        self.assertNotContains(response, "kode-rahasia")

    def test_add_without_a_code_bounces_back_to_the_form(self):
        response = self.client.post(self.add_url, self.without_code())

        self.assertRedirects(response, self.add_url)
        self.assertEqual(Project.objects.count(), 2)

    def test_add_with_a_wrong_code_bounces_back_to_the_form(self):
        response = self.client.post(self.add_url, self.payload | {"secret_code": "salah"})

        self.assertRedirects(response, self.add_url)
        self.assertEqual(Project.objects.count(), 2)

    def test_a_rejected_add_shows_the_warning(self):
        response = self.client.post(
            self.add_url, self.payload | {"secret_code": "salah"}, follow=True
        )

        self.assertContains(response, "Wrong or missing secret code.")
        self.assertContains(response, 'class="message error"')

    def test_add_with_the_right_code_saves_the_project(self):
        response = self.client.post(self.add_url, self.payload)

        self.assertRedirects(response, reverse("main:show_project"))
        self.assertEqual(Project.objects.count(), 3)
        self.assertEqual(Project.objects.get(name="Proyek Baru").kicker, "Buatan test")

    def test_the_code_is_never_written_to_the_model(self):
        self.client.post(self.add_url, self.payload)
        project = Project.objects.get(name="Proyek Baru")

        self.assertNotIn("kode-rahasia", str(project.__dict__))

    def test_a_right_code_still_has_to_pass_the_model_field_validation(self):
        response = self.client.post(self.add_url, self.payload | {"name": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), 2)
        self.assertContains(response, "form-error")

    def test_delete_without_a_code_keeps_the_project(self):
        project = Project.objects.first()

        response = self.client.post(reverse("main:delete_project", args=[project.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), 2)

    def test_delete_with_a_wrong_code_keeps_the_project(self):
        project = Project.objects.first()

        response = self.client.post(
            reverse("main:delete_project", args=[project.id]),
            {"secret_code": "salah"},
            follow=True,
        )

        self.assertContains(response, "Wrong or missing secret code.")
        self.assertEqual(Project.objects.count(), 2)
        self.assertTrue(Project.objects.filter(pk=project.id).exists())

    def test_delete_with_the_right_code_removes_the_project(self):
        project = Project.objects.first()

        response = self.client.post(
            reverse("main:delete_project", args=[project.id]), {"secret_code": "kode-rahasia"}
        )

        self.assertRedirects(response, reverse("main:show_project"))
        self.assertFalse(Project.objects.filter(pk=project.id).exists())

    def test_delete_of_a_missing_project_is_404(self):
        response = self.client.post(
            reverse("main:delete_project", args=[uuid.uuid4()]), {"secret_code": "kode-rahasia"}
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_confirmation_carries_its_own_code_field(self):
        response = self.client.get(reverse("main:show_project"))

        self.assertContains(response, 'name="secret_code"', count=Project.objects.count())


@override_settings(SECRET_CODE="")
class UnconfiguredSecretCodeTest(TestCase):
    """Setting kosong harus mengunci write, bukan justru membukanya."""

    def test_an_empty_setting_blocks_add(self):
        response = self.client.post(
            reverse("main:create_project"),
            {"name": "x", "description": "d", "order": 0, "secret_code": ""},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), 2)

    def test_an_empty_setting_blocks_delete(self):
        project = Project.objects.first()

        response = self.client.post(
            reverse("main:delete_project", args=[project.id]), {"secret_code": ""}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), 2)
