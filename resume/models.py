from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class PersonalInfo(models.Model):
    full_name = models.CharField(max_length=200)
    full_name_en = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    linkedin = models.CharField(max_length=200, blank=True)
    facebook = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.full_name


class Experience(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)
    company_en = models.CharField(max_length=200, blank=True)
    start_date = models.CharField(max_length=100, blank=True)
    end_date = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    description_en = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} @ {self.company}"


class Education(models.Model):
    degree = models.CharField(max_length=200)
    degree_en = models.CharField(max_length=200, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    institution_en = models.CharField(max_length=200, blank=True)
    period = models.CharField(max_length=100, blank=True)
    period_en = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Skill(models.Model):
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=60, blank=True, help_text='Optional category, e.g. software, other')

    def __str__(self):
        return self.name


class SoftwareSkill(models.Model):
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True)
    details = models.CharField(max_length=300, blank=True)
    details_en = models.CharField(max_length=300, blank=True)
    rating = models.PositiveSmallIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        verbose_name = 'Software Skill'
        verbose_name_plural = 'Software Skills'

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True)
    summary_en = models.TextField(blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title
