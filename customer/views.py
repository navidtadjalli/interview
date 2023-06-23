from http import HTTPStatus

from django.conf import settings
from rest_framework import generics, serializers, validators

from achare_interview.utils.validation_code import create_validation_code
from customer.models import Customer


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
    duration = serializers.IntegerField(
        read_only=True,
        default=settings.GENERATED_CODE_TIME_TO_LIVE
    )


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')

        create_validation_code(
            phone_number=serializer.validated_data.pop("phone_number"),
            ip=ip
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = HTTPStatus.OK

        return response
