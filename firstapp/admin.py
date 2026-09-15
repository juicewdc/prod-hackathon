from django.contrib import admin
from .models import ProjectUser


@admin.register(ProjectUser)
class ProjectUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
