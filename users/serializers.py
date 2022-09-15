from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("pk", "email", "first_name", "last_name", "avatar", "username", "role")
        read_only_fields = (
            "email",
            "username",
            "role",
        )

    def to_representation(self, instance):
        ret = super(UserDetailsSerializer, self).to_representation(instance)
        ret["role"] = [role[1] for role in User.user_roles if role[0] in instance.role][0]
        return ret
