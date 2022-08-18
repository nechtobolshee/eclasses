from rest_framework.permissions import BasePermission
from users.models import User
from rest_framework.response import Response
from rest_framework import status


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.EMPLOYEE
        )

    def has_object_permission(self, request, view, obj):
        try:
            return (
                bool(request.user in obj.class_name.students)
                if not bool(request.user in obj.students)
                else bool(request.user in obj.students)
            )
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.TEACHER
        )

    def has_object_permission(self, request, view, obj):
        try:
            return (
                bool(request.user == obj.class_name.teacher)
                if not bool(request.user == obj.teacher)
                else bool(request.user == obj.teacher)
            )
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)
