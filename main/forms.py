from django.core.exceptions import ValidationError
from django.forms import (
    CharField,
    ModelForm,
    NumberInput,
    PasswordInput,
    Textarea,
    TextInput,
    URLInput,
    DateInput,
    Select
)
from django.utils.html import strip_tags

from main.models import Experience, Achievement, Project

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "organization",
            "category", 
            "description",
            "started_at",
            "ended_at",
            "thumbnail",
        ]

        labels = {
            "title": "Posisi/Pekerjaan",
            "organization": "Organisasi/Perusahaan",
            "category": "Jenis Posisi/Pekerjaan",
            "description": "Deskripsi Posisi/Pekerjaan",
            "started_at": "Tanggal Mulai",
            "ended_at": "Tanggal Selesai (Kosongkan jika masih berlangsung)",
            "thumbnail": "URL Logo/Gambar (Opsional)",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Software Engineer",
                    "maxlength": 255
                }
            ),
            "organization": TextInput(
                attrs={
                    "placeholder": "Google",
                    "maxlength": 255
                }
            ),
            "category": Select(
                attrs={
                    "class": "form-control"
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Jelaskan peran dan tanggung jawab Anda...",
                    "rows": 4
                }
            ),
            "started_at": DateInput(
                attrs={
                    "type": "date"
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "date"
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://example.com/logo.png"
                }
            ),
        }

class AchievementForm(ModelForm):
    class Meta:
        model = Achievement
        fields = [
            "title",
            "organizer",
            "awarded_at",
            "certificate",
        ]

        labels = {
            "title": "Nama Penghargaan",
            "organizer": "Penyelenggara/Pemberi Penghargaan",
            "awarded_at": "Tanggal Pemberian Penghargaan",
            "certificate": "URL Gambar Sertifikat",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Achievement",
                    "maxlength": 255,
                }
            ),
            "organizer": TextInput(
                attrs={
                    "placeholder": "Organizer Name",
                    "maxlength": 255,
                }
            ),
            "awarded_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "certificate": URLInput(
                attrs={
                    "placeholder": "https://google.com/",
                }
            ),
        }

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "name",
            "kicker",
            "url",
            "description",
            "order",
        ]

        labels = {
            "name": "Nama Proyek",
            "kicker": "Label Singkat Tentang Proyek",
            "url": "URL Proyek",
            "description": "Deskripsi Proyek",
            "order": "Urutan Proyek dalam List (default value 0)",
        }

        widgets = {
            "name": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "kicker": TextInput(
                attrs={
                    "placeholder": "My Personal Website",
                    "maxlength": 100,
                }
            ),
            "url": URLInput(
                attrs={
                    "placeholder": "https://github.com/demtcsre/myportofolio",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Website yang berisi profil, penghargaan, pengalaman, serta portofolio.",
                    "rows": 3,
                }
            ),
            "order": NumberInput(
                attrs={
                    "placeholder": "0",
                    "min": 0,
                }
            ),
        }

    def clean_name(self):
        name = strip_tags(self.cleaned_data["name"]).strip()
        if not name:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return name

    def clean_kicker(self):
        return strip_tags(self.cleaned_data["kicker"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()
