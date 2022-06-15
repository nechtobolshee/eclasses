from django.urls import path
from .views import ClassListAPIView, CurrentClassesForStudentListAPIView, CurrentClassesForTeacherListAPIView


urlpatterns = [
    path('', ClassListAPIView.as_view(), name='classes-list'),
    path('student-my/', CurrentClassesForStudentListAPIView.as_view(), name='student-my'),
    path('teacher-my/', CurrentClassesForTeacherListAPIView.as_view(), name='teacher-my'),
]
