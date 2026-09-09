import uuid

from django.db import models


class Experience(models.Model):
    # LinkedIn's employment types, in LinkedIn's order.
    EXPERIENCE_CHOICES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('self-employed', 'Self-employed'),
        ('freelance', 'Freelance'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('apprenticeship', 'Apprenticeship'),
        ('seasonal', 'Seasonal'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateField()
    ended_at = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None


class Achievement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255, blank=True)
    awarded_at = models.DateField()
    certificate = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-awarded_at', 'title']

    def __str__(self):
        return self.title


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    kicker = models.CharField(max_length=100, blank=True, help_text="Small label above the title.")
    url = models.URLField(blank=True)
    description = models.TextField(help_text="Inline HTML links are allowed; rendered unescaped.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
