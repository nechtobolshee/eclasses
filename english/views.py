from .models import Class, Lessons
from django_filters.rest_framework import DjangoFilterBackend
from english.permissions import IsTeacher, IsEmployee
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    UpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
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


class CurrentClassesForStudentListAPIView(ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsEmployee]

    def get_queryset(self):
        return super().get_queryset().filter(students=self.request.user)


class CurrentClassesForTeacherListCreateAPIView(ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return super().get_queryset().filter(teacher=self.request.user)


class UpdateClassRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
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


class UpdateLessonRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return super().get_queryset().filter(class_name__teacher=self.request.user.pk, _status=Lessons.COMING_SOON)


class CurrentStudentToClassUpdateAPIView(UpdateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsEmployee]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.students.filter(id=self.request.user.id).exists():
            instance.students.remove(self.request.user)
        else:
            instance.students.add(self.request.user)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
