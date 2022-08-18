from rest_framework import serializers

from users.models import User
from .models import Class, Lessons, Schedule


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


class CreateClassSerializer(ClassSerializer):
    time_start = serializers.TimeField()
    time_end = serializers.TimeField()
    week_days = serializers.MultipleChoiceField(choices=Schedule.week_days)

    class Meta(ClassSerializer.Meta):
        fields = ("name", "students", "time_start", "time_end", "week_days")

    def create(self, validated_data: dict):
        obj_class = Class(
            name=validated_data.get("name"),
            teacher=self.context["request"].user
        )
        obj_class.save()
        obj_class.students.add(*validated_data.get("students"))

        schedule = Schedule(
            class_name=obj_class,
            start_time=validated_data.get("time_start"),
            end_time=validated_data.get("time_end"),
            days=list(validated_data.get('week_days'))
        )
        schedule.save()

        return obj_class

    def to_representation(self, instance):
        ret = super(CreateClassSerializer, self).to_representation(instance)
        ret["students"] = [UserSerializer(entry).data for entry in instance.students.all()]
        return ret


class DeleteClassSerializer(ClassSerializer):
    class Meta(ClassSerializer.Meta):
        fields = ("pk", "name", "students", "teacher")

    def to_representation(self, instance):
        ret = super(DeleteClassSerializer, self).to_representation(instance)
        ret["students"] = [UserSerializer(entry).data for entry in instance.students.all()]
        ret["teacher"] = UserSerializer(instance.teacher).data
        return ret


class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ("pk", "class_name", "_status", "time_start", "time_end")


class UpdateLessonSerializer(LessonsSerializer):
    class Meta(LessonsSerializer.Meta):
        fields = ("pk", "class_name", "_status", "time_start", "time_end")
        read_only_fields = ("pk", "class_name", "_status",)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["class_name"] = ClassSerializer(instance.class_name).data["name"]
        return ret
