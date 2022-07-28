from django.urls import path
from .views import (
    ClassListAPIView,
    CurrentClassesForStudentListAPIView,
    CurrentClassesForTeacherListAPIView,
    CurrentLessonsForStudentListAPIView,
    CurrentLessonsForTeacherListAPIView,
)


urlpatterns = [
    path("", ClassListAPIView.as_view(), name="classes-list"),
    path("student/classes", CurrentClassesForStudentListAPIView.as_view(), name="student-classes",),
    path("teacher/classes", CurrentClassesForTeacherListAPIView.as_view(), name="teacher-classes",),
    path("student/lessons", CurrentLessonsForStudentListAPIView.as_view(), name="student-lessons",),
    path("teacher/lessons", CurrentLessonsForTeacherListAPIView.as_view(), name="teacher-lessons",),
]
