from rest_framework.permissions import BasePermission
from users.models import User
from english.models import Class, Lessons


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.EMPLOYEE
        )

    def has_object_permission(self, request, view, obj):
        if obj == Class:
            return bool(request.user == obj.students)
        elif obj == Lessons:
            return bool(request.user == obj.class_name.students)


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.TEACHER
        )

    def has_object_permission(self, request, view, obj):
        if type(obj) == Class:
            return bool(request.user == obj.teacher)
        elif type(obj) == Lessons:
            return bool(request.user == obj.class_name.teacher)
