from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import User
from users.tz_convertation import (convert_datetime_to_user_timezone,
                                   convert_datetime_to_utc_timezone,
                                   convert_time_to_user_timezone,
                                   convert_time_to_utc_timezone)

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
        ret["start_time"] = convert_time_to_user_timezone(instance.start_time)
        ret["end_time"] = convert_time_to_user_timezone(instance.end_time)
        return ret

    def create(self, validated_data):
        validated_data["teacher"] = self.context["request"].user
        validated_data["start_time"] = convert_time_to_utc_timezone(validated_data["start_time"])
        validated_data["end_time"] = convert_time_to_utc_timezone(validated_data["end_time"])
        return super(ClassSerializer, self).create(validated_data)

    def validate(self, attrs):
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")
        if start_time and end_time and start_time > end_time:
            raise ValidationError("The start time can't be greater than the end time.")
        if (start_time and not end_time) or (end_time and not start_time):
            raise ValidationError("Please, fill in the start and end times.")
        if "days" in attrs:
            attrs["days"] = list(set(attrs["days"]))
            for day in attrs["days"]:
                if not 0 <= day < 8:
                    raise ValidationError("Incorrect selected days of the week.")
        return attrs


class LessonsSerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=15)

    class Meta:
        model = Lessons
        fields = ("pk", "class_name", "status", "start_time", "end_time")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["class_name"] = ClassSerializer(instance.class_name).data["name"]
        ret["start_time"] = convert_datetime_to_user_timezone(instance.start_time).strftime("%Y-%m-%d %H:%M")
        ret["end_time"] = convert_datetime_to_user_timezone(instance.end_time).strftime("%Y-%m-%d %H:%M")
        return ret

    def create(self, validated_data):
        validated_data.pop("status", None)
        validated_data["start_time"] = convert_datetime_to_utc_timezone(validated_data["start_time"])
        validated_data["end_time"] = convert_datetime_to_utc_timezone(validated_data["end_time"])
        return super(LessonsSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("class_name", None)
        if "status" in validated_data and validated_data["status"] != Lessons.CANCELED:
            raise ValidationError({"status": "Lesson status can be changed only to CANCELED."})
        if "start_time" in validated_data:
            validated_data["start_time"] = convert_datetime_to_utc_timezone(validated_data["start_time"])
        if "end_time" in validated_data:
            validated_data["end_time"] = convert_datetime_to_utc_timezone(validated_data["end_time"])
        instance = super(LessonsSerializer, self).update(instance, validated_data)
        return instance

    def validate(self, attrs):
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")
        if (start_time and not end_time) or (end_time and not start_time):
            raise ValidationError({"detail": "Please, fill in the start and end times."})
        if start_time and start_time < datetime.now():
            raise ValidationError({"start_time": "Start time should be larger than current time."})
        if start_time and end_time and start_time > end_time:
            raise ValidationError({"detail": "The start time can't be greater than the end time."})
        return attrs
