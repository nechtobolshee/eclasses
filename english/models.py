from django import forms
from django.contrib.postgres.fields import ArrayField
from django.db import models

from users.models import User


class Class(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    students = models.ManyToManyField(User, related_name="student_classes")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher_classes")

    class Meta:
        verbose_name_plural = "Class"

    def __str__(self):
        return self.name


class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class Schedule(models.Model):
    week_days = [
        ("1", "Monday"),
        ("2", "Tuesday"),
        ("3", "Wednesday"),
        ("4", "Thursday"),
        ("5", "Friday"),
        ("6", "Saturday"),
        ("7", "Sunday"),
    ]

    class_id = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name="Class name",
        related_name="class_name",
    )
    days = ChoiceArrayField(
        base_field=models.CharField(max_length=10, choices=week_days),
        default=list,
        size=5,
        blank=True,
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Schedule"
