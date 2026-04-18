import re

from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from rest_framework import serializers


class SendRechargeSerializer(serializers.Serializer):
    send_to = serializers.CharField(max_length=100)
    product = serializers.IntegerField()

    def validate_send_to(self, value: str) -> str:
        if re.fullmatch(r"\d{8}", value):
            return value

        try:
            validate_email(value)
            return value
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                "send_to must be a valid Cuba phone (+53########) or a valid email."
            ) from exc


class RechargeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.FloatField()
    type = serializers.CharField()


class UserDataSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
