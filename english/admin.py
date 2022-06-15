from django.contrib import admin

import english.models
from english.models import Class, Schedule


@admin.register(Class)
class AdminClass(admin.ModelAdmin):
    list_display = ("name", "teacher", "number_of_students")

    @staticmethod
    def number_of_students(obj):
        return obj.students.all().count()


@admin.register(Schedule)
class AdminSchedule(admin.ModelAdmin):
    list_display = ("class_id", "full_selected_days_name", "start_time", "end_time")

    @admin.display(description="Days")
    def full_selected_days_name(self, obj):
        all_days = english.models.Schedule.week_days
        selected_days = obj.days
        fullname_days = [item[1] for item in all_days if item[0] in selected_days]
        return fullname_days
