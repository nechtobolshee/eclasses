from django.contrib import admin, messages

from .models import Class, Schedule, Lessons


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
        return [item[1] for item in Schedule.week_days if item[0] in obj.days]

    @admin.display(description="Teacher")
    def get_teacher_name(self, obj):
        return obj.class_name.teacher


@admin.register(Lessons)
class AdminLessons(admin.ModelAdmin):
    list_display = ("class_name", "status", "time_start", "time_end")

    def save_model(self, request, obj, form, change):
        try:
            if "_status" in form.changed_data and "_status":
                obj.status = obj._status
            obj.save()
        except BaseException as e:
            messages.add_message(request, messages.ERROR, e)

    @admin.display(description="Status")
    def get_full_status(self, obj):
        return [item[1] for item in Lessons.status_choice if item[0] in obj.status]
