import json
import logging
import six
from datetime import datetime, timedelta
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import BadRequest, ValidationError
from django.db import models
from django.forms import MultipleChoiceField
from django.utils.translation import gettext_lazy as _
from english.calendar import CalendarManager
from users.models import User

logger = logging.getLogger('django')


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


class Class(models.Model):
    week_days = [
        (0, _("Monday")),
        (1, _("Tuesday")),
        (2, _("Wednesday")),
        (3, _("Thursday")),
        (4, _("Friday")),
        (5, _("Saturday")),
        (6, _("Sunday")),
    ]

    name = models.CharField(max_length=150, db_index=True, unique=True)
    students = models.ManyToManyField(User, related_name="student_classes")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher_classes")
    days = ChoiceArrayField(base_field=models.IntegerField(choices=week_days), default=list, size=5, blank=True)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Class"

    def __str__(self):
        return self.name

    def create_lessons(self):
        logger.info(f"Checking lessons for {self} class and starting to create new.")
        last_lesson = self.lessons.all().order_by("-end_time").first()
        date_from = last_lesson.end_time if last_lesson else datetime.now()
        date_end = datetime.now() + timedelta(weeks=4)
        if date_end.date() <= date_from.date():
            return

        lessons_to_create = list()
        for day in range(1, (date_end - date_from).days + 1):
            date = date_from + timedelta(days=day)
            if date.weekday() in self.days:
                lessons_to_create.append(Lessons(
                    class_name=self,
                    start_time=datetime.combine(date=date, time=self.start_time),
                    end_time=datetime.combine(date=date, time=self.end_time),
                ))
        if len(lessons_to_create) > 0:
            Lessons.objects.bulk_create(lessons_to_create)
            logger.warning(f"Created {len(lessons_to_create)} lessons for {self} class.")
        else:
            logger.warning(f"Lessons for {self} class have already been created. Nothing has changed.")


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
    google_event_id = models.CharField(max_length=150, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Lessons"
        ordering = ['start_time']

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
        if self.start_time > datetime.now():
            self._status = Lessons.COMING_SOON
        elif self.end_time > datetime.now() >= self.start_time:
            self.error_message(failed_status=Lessons.COMING_SOON, reason="going now")
        elif self.end_time <= datetime.now():
            self.error_message(failed_status=Lessons.COMING_SOON, reason="already ended")

    def set_status_progress(self):
        if self.end_time > datetime.now() >= self.start_time:
            self._status = Lessons.IN_PROGRESS
        elif self.start_time > datetime.now():
            self.error_message(failed_status=Lessons.IN_PROGRESS, reason="haven't started")
        elif self.end_time <= datetime.now():
            self.error_message(failed_status=Lessons.IN_PROGRESS, reason="already ended")

    def set_status_done(self):
        if self.end_time <= datetime.now():
            self._status = Lessons.DONE
        elif self.start_time > datetime.now():
            self.error_message(failed_status=Lessons.DONE, reason="haven't started")
        elif self.end_time > datetime.now() >= self.start_time:
            self.error_message(failed_status=Lessons.DONE, reason="going now")

    def set_status_canceled(self):
        if self._status != Lessons.DONE or self.end_time <= datetime.now():
            self._status = Lessons.CANCELED
        else:
            self.error_message(failed_status=Lessons.CANCELED, reason="already ended")

    def error_message(self, failed_status, reason):
        logger.warning(f"Tried to set {failed_status} status for {self.pk} lesson (event is {reason})")
        raise BadRequest(f"Can't set this {failed_status}, because this event is {reason}")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.google_event_id = CalendarManager().create_event(event_name=self.class_name.name, start_time=self.start_time, end_time=self.end_time)
        elif self._status == self.CANCELED:
            CalendarManager().delete_event(event_id=self.google_event_id)
        else:
            CalendarManager().update_event(event_id=self.google_event_id, start_time=self.start_time, end_time=self.end_time)
        super(Lessons, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        if self.google_event_id:
            CalendarManager().delete_event(event_id=self.google_event_id)
        super(Lessons, self).delete(using, keep_parents)
