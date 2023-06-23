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
        max_length=11,
        validators=[validators.UniqueValidator(Customer.objects.all())]
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
