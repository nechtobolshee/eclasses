from django.contrib import admin

from .models import Class, Schedule


@admin.register(Class)
class AdminClass(admin.ModelAdmin):
    list_display = ("name", "teacher", "number_of_students")

    @staticmethod
    def number_of_students(obj):
        return obj.students.all().count()


@admin.register(Schedule)
class AdminSchedule(admin.ModelAdmin):
    list_display = ("class_name", "get_teacher_name", "full_name_selected_days", "start_time", "end_time")

    @admin.display(description="Days")
    def full_name_selected_days(self, obj):
        full_name_days = [item[1] for item in Schedule.week_days if item[0] in obj.days]
        return full_name_days

    @admin.display(description="Teacher")
    def get_teacher_name(self, obj):
        teacher_name = obj.class_name.teacher
        return teacher_name
