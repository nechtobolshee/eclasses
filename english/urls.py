from django.urls import path
from .views import (
    ClassListAPIView,
    ClassesForStudentListAPIView,
    ClassesForTeacherListCreateAPIView,
    LessonsForStudentListAPIView,
    LessonsForTeacherListCreateAPIView,
    ClassForTeacherRetrieveUpdateDestroyAPIView,
    LessonForTeacherRetrieveUpdateAPIView,
    JoinToClassUpdateDestroyAPIView,
)


urlpatterns = [
    path("", ClassListAPIView.as_view(), name="classes-list"),

    path("student/classes/<int:pk>/join/", JoinToClassUpdateDestroyAPIView.as_view(), name="join-to-class"),
    path("student/classes/", ClassesForStudentListAPIView.as_view(), name="student-classes-list"),
    path("student/lessons/", LessonsForStudentListAPIView.as_view(), name="student-lessons-list"),

    path("teacher/classes/<int:pk>/", ClassForTeacherRetrieveUpdateDestroyAPIView.as_view(), name="teacher-classes-retrive-update-destroy"),
    path("teacher/classes/", ClassesForTeacherListCreateAPIView.as_view(), name="teacher-classes-list-create"),
    path("teacher/lessons/<int:pk>/", LessonForTeacherRetrieveUpdateAPIView.as_view(), name="teacher-lesson-retrive-update"),
    path("teacher/lessons/", LessonsForTeacherListCreateAPIView.as_view(), name="teacher-lessons-list-create"),
]
