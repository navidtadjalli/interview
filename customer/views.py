from http import HTTPStatus

from rest_framework import generics
from rest_framework.response import Response

from achare_interview.utils.validation_code import create_validation_code
from customer.serializers import AuthenticateSerializer


class AuthenticateAPIView(generics.GenericAPIView):
    serializer_class = AuthenticateSerializer

    def send_code(self, serializer):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')

        create_validation_code(
            phone_number=serializer.validated_data.pop("phone_number"),
            ip=ip
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.send_code(serializer)
        return Response(serializer.data, status=HTTPStatus.OK)


class ValidateAPIView(generics.GenericAPIView):
    pass
