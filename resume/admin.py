from django.contrib import admin
from .models import PersonalInfo, Experience, Education, Skill, Project, SoftwareSkill
from .models import PreferredAI

@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'email')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'end_date')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'period')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')


@admin.register(SoftwareSkill)
class SoftwareSkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating')


@admin.register(PreferredAI)
class PreferredAIAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
