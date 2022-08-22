from django.contrib import admin, messages

from .models import Class, Lessons


@admin.register(Class)
class AdminClass(admin.ModelAdmin):
    list_display = ("name", "teacher", "full_name_selected_days", "number_of_students")

    @staticmethod
    def number_of_students(obj):
        return obj.students.all().count()

    @admin.display(description="Days")
    def full_name_selected_days(self, obj):
        return [day[1] for day in Class.week_days if day[0] in obj.days]


@admin.register(Lessons)
class AdminLessons(admin.ModelAdmin):
    list_display = ("class_name", "status", "time_start", "time_end")

    def save_model(self, request, obj, form, change):
        try:
            if "_status" in form.changed_data:
                obj.status = obj._status
            obj.save()
        except BaseException as e:
            messages.add_message(request, messages.ERROR, e)
