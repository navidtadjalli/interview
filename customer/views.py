from http import HTTPStatus

from rest_framework import generics

from achare_interview.utils.validation_code import create_validation_code
from customer.serializers import AuthenticateSerializer


class AuthenticateAPIView(generics.CreateAPIView):
    serializer_class = AuthenticateSerializer

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
