from django.urls import path
from .views import ClassListAPIView, CurrentClassesForStudentAPIView, CurrentClassesForTeacherAPIView


urlpatterns = [
    path('list-all/', ClassListAPIView.as_view(), name='classes_list'),
    path('student-my/', CurrentClassesForStudentAPIView.as_view()),
    path('teacher-my/', CurrentClassesForTeacherAPIView.as_view()),
]
