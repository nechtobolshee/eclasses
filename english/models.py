from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.forms import MultipleChoiceField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import BadRequest, ValidationError
from users.models import User
from datetime import datetime
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


class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": MultipleChoiceField,
            "choices": self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class Schedule(models.Model):
    week_days = [
        ("1", _("Monday")),
        ("2", _("Tuesday")),
        ("3", _("Wednesday")),
        ("4", _("Thursday")),
        ("5", _("Friday")),
        ("6", _("Saturday")),
        ("7", _("Sunday")),
    ]

    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="Class name", related_name="class_name")
    days = ChoiceArrayField(base_field=models.CharField(max_length=10, choices=week_days), default=list, size=5, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

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

    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="class_name")
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
            logger.warning(f"Tried to set {Lessons.COMING_SOON} status for {self.pk} lesson (event is going now)")
            raise BadRequest("Can't set this status, because this event is going now")
        elif self.time_end <= datetime.now():
            logger.warning(f"Tried to set {Lessons.COMING_SOON} status for {self.pk} lesson (event is already ended)")
            raise BadRequest("Can't set this status, because this event is already ended")

    def set_status_progress(self):
        if self.time_end > datetime.now() >= self.time_start:
            self._status = Lessons.IN_PROGRESS
        elif self.time_start > datetime.now():
            logger.warning(f"Tried to set {Lessons.IN_PROGRESS} status for {self.pk} lesson (event is haven't started)")
            raise BadRequest("Can't set this status, because this event is haven't started")
        elif self.time_end <= datetime.now():
            logger.warning(f"Tried to set {Lessons.IN_PROGRESS} status for {self.pk} lesson (event is already ended)")
            raise BadRequest("Can't set this status, because this event is already ended")

    def set_status_done(self):
        if self.time_end <= datetime.now():
            self._status = Lessons.DONE
        elif self.time_start > datetime.now():
            logger.warning(f"Tried to set {Lessons.DONE} status for {self.pk} lesson (event is haven't started)")
            raise BadRequest("Can't set this status, because this event is haven't started")
        elif self.time_end > datetime.now() >= self.time_start:
            logger.warning(f"Tried to set {Lessons.DONE} status for {self.pk} lesson (event is going now)")
            raise BadRequest("Can't set this status, because this event is going now")

    def set_status_canceled(self):
        if self._status != Lessons.DONE or self.time_end <= datetime.now():
            self._status = Lessons.CANCELED
        else:
            logger.warning(f"Tried to set {Lessons.CANCELED} status for {self.pk} lesson (event is already ended)")
            raise BadRequest("Can't set this status, because this event is already ended")
