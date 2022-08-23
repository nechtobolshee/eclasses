from .models import Class, Lessons
from django_filters.rest_framework import DjangoFilterBackend
from english.permissions import IsTeacher, IsEmployee
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    UpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView
)
from .serializers import (
    ClassSerializer,
    LessonsSerializer,
)


class ClassListAPIView(ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'teacher', 'students']


class JoinToClassUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.students.add(self.request.user)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.students.filter(id=self.request.user.id).exists():
            instance.students.remove(self.request.user)
            instance.save()
        return Response(status=status.HTTP_200_OK)


class ClassesForStudentListAPIView(ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsEmployee]

    def get_queryset(self):
        return super().get_queryset().filter(students=self.request.user)


class LessonsForStudentListAPIView(ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated, IsEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_name']

    def get_queryset(self):
        return super().get_queryset().filter(class_name__students=self.request.user.pk, _status__in=[Lessons.COMING_SOON, Lessons.IN_PROGRESS])


class ClassesForTeacherListCreateAPIView(ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return super().get_queryset().filter(teacher=self.request.user)


class ClassForTeacherRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return super().get_queryset().filter(teacher=self.request.user)


class LessonsForTeacherListAPIView(ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_name']

    def get_queryset(self):
        return super().get_queryset().filter(class_name__teacher=self.request.user.pk, _status__in=[Lessons.COMING_SOON, Lessons.IN_PROGRESS])


class LessonForTeacherRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return super().get_queryset().filter(class_name__teacher=self.request.user.pk, _status=Lessons.COMING_SOON)
