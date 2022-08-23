from rest_framework import serializers
from django.core.exceptions import ValidationError

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

    def create(self, validated_data):
        validated_data["teacher"] = self.context["request"].user
        return super(ClassSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("teacher", None)
        return super(ClassSerializer, self).update(instance, validated_data)

    def validate(self, attrs):
        if "start_time" in attrs and "end_time" in attrs and attrs["start_time"] > attrs["end_time"]:
            raise ValidationError("The start time can't be greater than the end time.")
        if ("start_time" in attrs and "end_time" not in attrs) or \
                ("start_time" not in attrs and "end_time" in attrs):
            raise ValidationError("Please, fill in the start and end times.")
        if "days" in attrs:
            attrs["days"] = list(set(attrs["days"]))
            for day in attrs["days"]:
                if not 0 <= day < 8:
                    raise ValidationError("Incorrect selected days of the week.")
        return attrs


class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ("pk", "class_name", "_status", "time_start", "time_end")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["class_name"] = ClassSerializer(instance.class_name).data["name"]
        return ret

    def update(self, instance, validated_data):
        validated_data.pop("class_name", None)
        if validated_data.get("status") and validated_data["status"] != Lessons.CANCELED:
            raise ValidationError("Lesson status can be changed only to CANCELED.")
        return super(LessonsSerializer, self).update(instance, validated_data)

    def validate(self, attrs):
        if "time_start" in attrs and "time_end" in attrs and attrs["time_start"] > attrs["time_end"]:
            raise ValidationError("The start time can't be greater than the end time.")
        if ("start_time" in attrs and "end_time" not in attrs) or \
                ("start_time" not in attrs and "end_time" in attrs):
            raise ValidationError("Please, fill in the start and end times.")
        return attrs
