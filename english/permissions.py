from rest_framework.permissions import BasePermission
from users.models import User


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == User.EMPLOYEE
        )

    def has_object_permission(self, request, view, obj):
        is_employee = self.has_permission(request, view)
        return bool(is_employee and request.user in obj.students)


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == User.TEACHER
        )

    def has_object_permission(self, request, view, obj):
        is_teacher = self.has_permission(request, view)
        return bool(is_teacher and obj.teacher == request.user)
