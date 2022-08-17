from rest_framework.generics import ListAPIView
from .serializers import ClassSerializer, LessonsSerializer
from .models import Class, Lessons
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from english.permissions import IsTeacher, IsEmployee


class ClassListAPIView(ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'teacher', 'students']


class CurrentClassesForStudentListAPIView(ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsEmployee]

    def get_queryset(self):
        return super().get_queryset().filter(students=self.request.user)


class CurrentClassesForTeacherListAPIView(ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return super().get_queryset().filter(teacher=self.request.user)


class CurrentLessonsForStudentListAPIView(ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated, IsEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_name']

    def get_queryset(self):
        return super().get_queryset().filter(class_name__students=self.request.user.pk, _status__in=[Lessons.COMING_SOON, Lessons.IN_PROGRESS])


class CurrentLessonsForTeacherListAPIView(ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_name']

    def get_queryset(self):
        return super().get_queryset().filter(class_name__teacher=self.request.user.pk, _status__in=[Lessons.COMING_SOON, Lessons.IN_PROGRESS])
