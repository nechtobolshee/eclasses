from django.contrib import admin

from english.models import Class


@admin.register(Class)
class AdminClass(admin.ModelAdmin):
    list_display = ("name", "teacher", "number_of_students")

    @staticmethod
    def number_of_students(obj):
        return obj.students.all().count()
