from django.contrib import admin
from django.contrib.admin.options import ModelAdmin


# Register your models here.
from projects.models import Project, Review, Tag


class ProjectAdmin(ModelAdmin):
    list_display = ["title", "description", "demo_link", "source_link"]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Review)
admin.site.register(Tag)
