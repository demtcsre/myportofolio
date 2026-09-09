"""Seed the content that used to be hardcoded in templates/index.html.

Runs on migrate, so a fresh clone or a fresh PWS database comes up with the
same page the static template used to render.
"""

import datetime
import uuid

from django.db import migrations

EXPERIENCES = [
    {
        'title': 'Teaching Assistant · Programming Foundation 1 (DDP1)',
        'organization': 'Fakultas Ilmu Komputer, Universitas Indonesia',
        'description': 'Undergraduate TA for the introductory programming (Python) course.',
        'category': 'part-time',
        'started_at': datetime.date(2026, 8, 1),
    },
    {
        'title': 'CTF Staff · COMPFEST 18',
        'organization': 'Universitas Indonesia',
        'description': 'Problem setter for reverse engineering and binary exploitation, plus frontend and technical work.',
        'category': 'volunteer',
        'started_at': datetime.date(2026, 4, 1),
    },
    {
        'title': 'Member · NetSOS SIG',
        'organization': 'RISTEK Fakultas Ilmu Komputer, Universitas Indonesia',
        'description': 'PIC of Pekan Ristek 2026 CTF Competition',
        'category': 'volunteer',
        'started_at': datetime.date(2026, 3, 1),
    },
]

ACHIEVEMENTS = [
    {
        'title': '1st place · POLRI CTF 2026',
        'organizer': 'E-Sport Kapolri Cup, with SiberLab.id',
        'awarded_at': datetime.date(2026, 8, 1),
        'certificate': '/static/img/cert/polri-ctf-2026.png',
    },
    {
        'title': 'Finalist · Wreck-IT 7.0 CTF',
        'organizer': 'Politeknik Siber dan Sandi Negara',
        'awarded_at': datetime.date(2026, 8, 1),
        'certificate': '/static/img/cert/wreckit-7-2026.png',
    },
    {
        'title': 'Finalist · FindIT! 2026 CTF',
        'organizer': 'KMTETI, Fakultas Teknik UGM',
        'awarded_at': datetime.date(2026, 5, 1),
        'certificate': '/static/img/cert/findit-2026.png',
    },
]

PROJECTS = [
    {
        'order': 0,
        'kicker': 'Pwn tooling',
        'name': 'pwninit.py-demtcsre',
        'url': 'https://github.com/demtcsre/pwninit.py-demtcsre',
        'description': (
            'A tool for automating the setup of binary exploitation challenges. A port of '
            '<a href="https://github.com/sasha-999/pwninit.py">sasha-999/pwninit.py</a>, '
            'brought up to what the current '
            '<a href="https://github.com/io12/pwninit">io12/pwninit</a> does.'
        ),
    },
    {
        'order': 1,
        'kicker': 'A/D CTF Flag Farm',
        'name': 'S4DFarm-demtcsre',
        'url': 'https://github.com/demtcsre/S4DFarm-demtcsre',
        'description': (
            'A flag farm for the Attack and Defense CTF format, forked from '
            '<a href="https://github.com/C4T-BuT-S4D/S4DFarm">C4T-BuT-S4D/S4DFarm</a> '
            'and reshaped around how I actually run a round. It got its first real '
            'outing at the PolriCTF 2026 final.'
        ),
    },
]

SEED = [('Experience', EXPERIENCES), ('Achievement', ACHIEVEMENTS), ('Project', PROJECTS)]


# ponytail: derive the primary keys instead of letting uuid4 roll fresh ones per
# database. Local SQLite and the PWS Postgres then agree on ids, so a dumpdata /
# loaddata between them updates these rows instead of duplicating them.
SITE = 'https://ahmad-rizki53-myportofolio.pws.cs.ui.ac.id/'


def seed_id(model_name, key):
    return uuid.uuid5(uuid.NAMESPACE_URL, SITE + model_name + '/' + key)


def seed(apps, schema_editor):
    for model_name, rows in SEED:
        model = apps.get_model('main', model_name)
        model.objects.bulk_create([
            model(id=seed_id(model_name, row.get('title') or row['name']), **row)
            for row in rows
        ])


def unseed(apps, schema_editor):
    apps.get_model('main', 'Experience').objects.filter(
        title__in=[row['title'] for row in EXPERIENCES]).delete()
    apps.get_model('main', 'Achievement').objects.filter(
        title__in=[row['title'] for row in ACHIEVEMENTS]).delete()
    apps.get_model('main', 'Project').objects.filter(
        name__in=[row['name'] for row in PROJECTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_achievement_project_alter_experience_options_and_more'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
