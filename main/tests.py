import datetime

from django.test import TestCase
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
