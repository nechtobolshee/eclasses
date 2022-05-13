from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("pk", "email", "first_name", "last_name", "avatar")
        read_only_fields = (
            "email",
            "username",
        )
