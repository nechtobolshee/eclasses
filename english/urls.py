from django.urls import path
from .views import (
    ClassListAPIView,
    CurrentClassesForStudentListAPIView,
    CurrentClassesForTeacherListAPIView,
    CurrentLessonsForStudentListAPIView,
    CurrentLessonsForTeacherListAPIView,
    ClassesAndScheduleCreateAPIView,
    ClassesScheduleLessonsRetrieveDestroyAPIView,
    UpdateLessonsForTeacherRetrieveUpdateAPIView
)


urlpatterns = [
    path("", ClassListAPIView.as_view(), name="classes-list"),
    path("student/classes", CurrentClassesForStudentListAPIView.as_view(), name="student-classes",),
    path("teacher/classes", CurrentClassesForTeacherListAPIView.as_view(), name="teacher-classes",),
    path("student/lessons", CurrentLessonsForStudentListAPIView.as_view(), name="student-lessons",),
    path("teacher/lessons", CurrentLessonsForTeacherListAPIView.as_view(), name="teacher-lessons",),
    path("teacher/classes/create", ClassesAndScheduleCreateAPIView.as_view(), name="create-classes", ),
    path("teacher/classes/delete/<int:pk>", ClassesScheduleLessonsRetrieveDestroyAPIView.as_view(), name="delete-classes"),
    path("teacher/lessons/update/<int:pk>", UpdateLessonsForTeacherRetrieveUpdateAPIView.as_view(), name="update-lessons")
]
