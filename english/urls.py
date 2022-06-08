from django.urls import path
from .views import ClassListAPIView, CurrentClassesForStudentAPIView, CurrentClassesForTeacherAPIView


urlpatterns = [
    path('classes/list/', ClassListAPIView.as_view()),
    path('student/my/', CurrentClassesForStudentAPIView.as_view()),
    path('teacher/my/', CurrentClassesForTeacherAPIView.as_view()),
]
