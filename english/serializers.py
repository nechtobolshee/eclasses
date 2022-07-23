from .models import Class, Lessons
from users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "first_name", "last_name")


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ("pk", "name", "students", "teacher")

    def to_representation(self, instance):
        ret = super(ClassSerializer, self).to_representation(instance)
        ret["teacher"] = UserSerializer(instance.teacher).data
        ret["students"] = [UserSerializer(entry).data for entry in instance.students.all()]
        return ret


class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ("pk", "class_name", "_status", "time_start", "time_end")

    def to_representation(self, instance):
        ret = super(LessonsSerializer, self).to_representation(instance)
        ret["_status"] = [item[1] for item in Lessons.status_choice if item[0] in instance._status][0]
        return ret
    