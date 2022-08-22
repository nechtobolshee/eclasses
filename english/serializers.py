from rest_framework import serializers

from users.models import User
from .models import Class, Lessons


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "first_name", "last_name")


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ("pk", "name", "students", "teacher", "days", "start_time", "end_time")
        read_only_fields = ("teacher",)

    def to_representation(self, instance):
        ret = super(ClassSerializer, self).to_representation(instance)
        ret["teacher"] = UserSerializer(instance.teacher).data
        ret["students"] = [UserSerializer(entry).data for entry in instance.students.all()]
        ret["days"] = [day[1] for day in Class.week_days if day[0] in instance.days]
        return ret


class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ("pk", "class_name", "_status", "time_start", "time_end")
        read_only_fields = ("pk", "class_name", "_status",)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["class_name"] = ClassSerializer(instance.class_name).data["name"]
        return ret
