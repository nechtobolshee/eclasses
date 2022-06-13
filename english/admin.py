from django.contrib import admin

from english.models import Class


@admin.register(Class)
class AdminClass(admin.ModelAdmin):
    list_display = ("name", "get_teacher")

    def get_teacher(self, obj):
        teacher = obj.teacher.get_full_name()
        return teacher

    get_teacher.short_description = "Teacher"
