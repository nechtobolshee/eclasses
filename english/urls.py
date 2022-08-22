from django.urls import path
from .views import (
    ClassListAPIView,
    CurrentClassesForStudentListAPIView,
    CurrentClassesForTeacherListCreateAPIView,
    CurrentLessonsForStudentListAPIView,
    CurrentLessonsForTeacherListAPIView,
    UpdateClassRetrieveDestroyAPIView,
    UpdateLessonRetrieveUpdateAPIView,
    CurrentStudentToClassUpdateAPIView,
)


urlpatterns = [
    path("", ClassListAPIView.as_view(), name="classes-list"),
    path("student/classes/", CurrentClassesForStudentListAPIView.as_view(), name="student-classes"),
    path("student/lessons/", CurrentLessonsForStudentListAPIView.as_view(), name="student-lessons"),
    path("student/classes/<int:pk>/join-success/", CurrentStudentToClassUpdateAPIView.as_view(), name="join-class"),

    path("teacher/classes/", CurrentClassesForTeacherListCreateAPIView.as_view(), name="teacher-classes"),
    path("teacher/classes?id=<int:pk>/change/", UpdateClassRetrieveDestroyAPIView.as_view(), name="change-class"),
    path("teacher/lessons/", CurrentLessonsForTeacherListAPIView.as_view(), name="teacher-lessons"),
    path("teacher/lessons?id=<int:pk>/change/", UpdateLessonRetrieveUpdateAPIView.as_view(), name="change-lesson")
]
