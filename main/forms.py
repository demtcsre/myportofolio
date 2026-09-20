from django.forms import (
    CharField,
    ModelForm,
    NumberInput,
    PasswordInput,
    Textarea,
    TextInput,
    URLInput,
)

from main.models import Project


class ProjectForm(ModelForm):
    secret_code = CharField(
        label="Secret Code",
        widget=PasswordInput(attrs={"autocomplete": "off"}),
    )

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
