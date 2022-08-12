from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.forms import MultipleChoiceField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import BadRequest, ValidationError
from users.models import User
from datetime import datetime, timedelta
import six
import json
import logging

logger = logging.getLogger('django')


class Class(models.Model):
    name = models.CharField(max_length=150, db_index=True, unique=True)
    students = models.ManyToManyField(User, related_name="student_classes")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher_classes")

    class Meta:
        verbose_name_plural = "Class"

    def __str__(self):
        return self.name

    def create_lessons(self):
        selected_schedule = self.schedule
        last_lesson = self.lessons.filter(class_name=selected_schedule.class_name).order_by("-time_end").first()
        date_from = last_lesson.time_end if last_lesson else datetime.now()
        date_end = datetime.now() + timedelta(weeks=4)
        if date_end.date() <= date_from.date():
            return

        lessons_to_create = list()
        scheduled_days = selected_schedule.days
        for day in range(1, (date_end - date_from).days + 1):
            date = date_from + timedelta(days=day)
            if date.weekday() in scheduled_days:
                lessons_to_create.append(Lessons(
                    class_name=self,
                    time_start=datetime.combine(date=date, time=selected_schedule.start_time),
                    time_end=datetime.combine(date=date, time=selected_schedule.end_time),
                ))
        if len(lessons_to_create) > 0:
            logger.info(f"Created {len(lessons_to_create)} lessons for {self} class.")
            return Lessons.objects.bulk_create(lessons_to_create)


class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": MultipleChoiceField,
            "choices": self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)

    def to_python(self, value):
        if isinstance(value, six.string_types):
            value = [self.base_field.to_python(val) for val in json.loads(value)]
        elif isinstance(value, list):
            value = [self.base_field.to_python(val) for val in value]
        return value


class Schedule(models.Model):
    week_days = [
        (0, _("Monday")),
        (1, _("Tuesday")),
        (2, _("Wednesday")),
        (3, _("Thursday")),
        (4, _("Friday")),
        (5, _("Saturday")),
        (6, _("Sunday")),
    ]

    class_name = models.OneToOneField(Class, on_delete=models.CASCADE, verbose_name="Class name", related_name="schedule")
    days = ChoiceArrayField(base_field=models.IntegerField(choices=week_days), default=list, size=5, blank=True)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Schedule"

    def __str__(self):
        return self.class_name.name


class Lessons(models.Model):
    COMING_SOON = "COMING"
    IN_PROGRESS = "PROGRESS"
    DONE = "DONE"
    CANCELED = "CANCELED"

    status_choice = [
        (COMING_SOON, _("Coming soon..")),
        (IN_PROGRESS, _("In progress")),
        (DONE, _("Done")),
        (CANCELED, _("Canceled"))
    ]

    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="class_name", related_name="lessons")
    _status = models.CharField(max_length=15, choices=status_choice, default=COMING_SOON)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Lessons"
        ordering = ['time_start']

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        dispatcher = {
            self.COMING_SOON: self.set_status_coming,
            self.IN_PROGRESS: self.set_status_progress,
            self.DONE: self.set_status_done,
            self.CANCELED: self.set_status_canceled
        }
        if value in dispatcher.keys():
            dispatcher[value]()
            self.save()
        else:
            logger.warning(f"Tried to set not allowed status for {self.pk} lesson (status: {value})")
            raise ValidationError("Wrong status.. Please, set allowed status")

    def set_status_coming(self):
        if self.time_start > datetime.now():
            self._status = Lessons.COMING_SOON
        elif self.time_end > datetime.now() >= self.time_start:
            self.error_message(failed_status=Lessons.COMING_SOON, reason="going now")
        elif self.time_end <= datetime.now():
            self.error_message(failed_status=Lessons.COMING_SOON, reason="already ended")

    def set_status_progress(self):
        if self.time_end > datetime.now() >= self.time_start:
            self._status = Lessons.IN_PROGRESS
        elif self.time_start > datetime.now():
            self.error_message(failed_status=Lessons.IN_PROGRESS, reason="haven't started")
        elif self.time_end <= datetime.now():
            self.error_message(failed_status=Lessons.IN_PROGRESS, reason="already ended")

    def set_status_done(self):
        if self.time_end <= datetime.now():
            self._status = Lessons.DONE
        elif self.time_start > datetime.now():
            self.error_message(failed_status=Lessons.DONE, reason="haven't started")
        elif self.time_end > datetime.now() >= self.time_start:
            self.error_message(failed_status=Lessons.DONE, reason="going now")

    def set_status_canceled(self):
        if self._status != Lessons.DONE or self.time_end <= datetime.now():
            self._status = Lessons.CANCELED
        else:
            self.error_message(failed_status=Lessons.CANCELED, reason="already ended")

    def error_message(self, failed_status, reason):
        logger.warning(f"Tried to set {failed_status} status for {self.pk} lesson (event is {reason})")
        raise BadRequest(f"Can't set this {failed_status}, because this event is {reason}")
