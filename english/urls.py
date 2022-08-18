from django.urls import path
from .views import (
    ClassListAPIView,
    CurrentClassesForStudentListAPIView,
    CurrentClassesForTeacherListAPIView,
    CurrentLessonsForStudentListAPIView,
    CurrentLessonsForTeacherListAPIView,
    ClassesAndScheduleCreateAPIView,
    ClassesScheduleLessonsRetrieveDestroyAPIView,
    UpdateLessonsRetrieveUpdateAPIView
)


urlpatterns = [
    path("", ClassListAPIView.as_view(), name="classes-list"),
    path("classes/student/", CurrentClassesForStudentListAPIView.as_view(), name="student-classes",),
    path("classes/teacher/", CurrentClassesForTeacherListAPIView.as_view(), name="teacher-classes",),
    path("classes/create/", ClassesAndScheduleCreateAPIView.as_view(), name="create-classes", ),
    path("classes/<int:pk>/change/", ClassesScheduleLessonsRetrieveDestroyAPIView.as_view(), name="change-class"),
    path("lessons/student/", CurrentLessonsForStudentListAPIView.as_view(), name="student-lessons",),
    path("lessons/teacher/", CurrentLessonsForTeacherListAPIView.as_view(), name="teacher-lessons",),
    path("lessons/<int:pk>/change/", UpdateLessonsRetrieveUpdateAPIView.as_view(), name="change-lesson")
]
