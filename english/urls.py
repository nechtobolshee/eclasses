from django.urls import path
from .views import ClassListAPIView, CurrentClassesForStudentAPIView, CurrentClassesForTeacherAPIView


urlpatterns = [
    path('list-all/', ClassListAPIView.as_view(), name='classes-all'),
    path('student-my/', CurrentClassesForStudentAPIView.as_view(), name='student-my'),
    path('teacher-my/', CurrentClassesForTeacherAPIView.as_view(), name='teacher-my'),
]
