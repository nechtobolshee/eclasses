from rest_framework.generics import ListAPIView
from .serializers import ClassSerializer
from english.models import Class
# from english.permissions import IsAdminUserOrReadOnly
from rest_framework.permissions import IsAuthenticated


class ClassListAPIView(ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]


class CurrentClassesForStudentAPIView(ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(students=self.request.user)


class CurrentClassesForTeacherAPIView(ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(teacher=self.request.user)
