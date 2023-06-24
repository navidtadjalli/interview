from django.conf import settings
from rest_framework import serializers, validators

from customer.models import Customer


class AuthenticateSerializer(serializers.Serializer):
    phone_number = serializers.RegexField(
        allow_blank=False,
        allow_null=False,
        required=True,
        write_only=True,
        regex=r'^09\d+$',
        min_length=11,
        max_length=11
    )
    duration = serializers.IntegerField(
        read_only=True,
        default=settings.GENERATED_CODE_TIME_TO_LIVE
    )


class ValidateSerializer(serializers.Serializer):
    phone_number = serializers.RegexField(
        allow_blank=False,
        allow_null=False,
        required=True,
        write_only=True,
        regex=r'^09\d+$',
        min_length=11,
        max_length=11,
        validators=[validators.UniqueValidator(Customer.objects.all())]
    )
    code = serializers.RegexField(
        allow_blank=False,
        allow_null=False,
        required=True,
        write_only=True,
        regex=r'^\d+$',
        min_length=6,
        max_length=6
    )


class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.RegexField(
        allow_blank=False,
        allow_null=False,
        required=True,
        write_only=True,
        regex=r'^09\d+$',
        min_length=11,
        max_length=11,
        validators=[validators.UniqueValidator(Customer.objects.all())]
    )
    email = serializers.EmailField(
        allow_blank=True,
        allow_null=True,
        required=False,
        write_only=True
    )
    first_name = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        required=True,
        write_only=True,
        min_length=3,
        max_length=150
    )
    last_name = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        required=True,
        write_only=True,
        min_length=3,
        max_length=150
    )
    password = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        required=True,
        write_only=True
    )
    registration_token = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        required=True,
        write_only=True,
        min_length=32,
        max_length=32
    )
