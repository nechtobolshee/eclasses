from .models import Class, Lessons, Schedule
from django_filters.rest_framework import DjangoFilterBackend
from english.permissions import IsTeacher, IsEmployee
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView
)
from .serializers import (
    ClassSerializer,
    LessonsSerializer,
    CreateClassSerializer,
    DeleteClassSerializer,
    UpdateLessonSerializer
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


class CurrentClassesForTeacherListAPIView(ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return super().get_queryset().filter(teacher=self.request.user)


class ClassesAndScheduleCreateAPIView(CreateAPIView):
    serializer_class = CreateClassSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class ClassesScheduleLessonsRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = DeleteClassSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return super().get_queryset().filter(teacher=self.request.user)

    def destroy(self, request, *args, **kwargs):
        class_instance = self.get_object()
        schedule_instance = Schedule.objects.all().filter(class_name=class_instance.pk)
        lessons_instance = Lessons.objects.all().filter(class_name=class_instance.pk)
        self.perform_destroy(class_instance)
        self.perform_destroy(schedule_instance)
        self.perform_destroy(lessons_instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class UpdateLessonsForTeacherRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = UpdateLessonSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return super().get_queryset().filter(class_name__teacher=self.request.user.pk, _status=Lessons.COMING_SOON)
