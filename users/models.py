from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import logging

logger = logging.getLogger('django')


class User(AbstractUser):
    EMPLOYEE = "EMPLOYEE"
    TEACHER = "TEACHER"
    HR = "HR"

    user_roles = [
        (EMPLOYEE, _("Employee")),
        (TEACHER, _("Teacher")),
        (HR, _("HR")),
    ]

    avatar = models.ImageField(upload_to='uploads/', blank=True)
    _role = models.CharField(max_length=10, null=False, choices=user_roles, default=EMPLOYEE)

    def __str__(self):
        return self.get_full_name() if (self.first_name and self.last_name) else self.username

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if value == User.HR:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        logger.info(f"Changed role for {self.get_full_name()} (id: {self.pk}) to '{value}'")
        self.save()
