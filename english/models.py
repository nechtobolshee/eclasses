from django.db import models
from users.models import User


class Class(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    students = models.ManyToManyField(User, related_name="student_classes")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher_classes")

    class Meta:
        verbose_name_plural = "Class"
