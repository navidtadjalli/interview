from http import HTTPStatus

from rest_framework import generics
from rest_framework.response import Response

from achare_interview.utils import exceptions, error_messages
from achare_interview.utils.validation_code import create_validation_code, validate_validation_code
from customer import serializers


class AuthenticateAPIView(generics.GenericAPIView):
    serializer_class = serializers.AuthenticateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_validation_code(phone_number=serializer.validated_data.pop("phone_number"))
        return Response(serializer.data, status=HTTPStatus.OK)


class ValidateAPIView(generics.GenericAPIView):
    serializer_class = serializers.ValidateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            validate_validation_code(
                phone_number=serializer.validated_data.pop("phone_number"),
                code=serializer.validated_data.pop("code")
            )
        except exceptions.ValidationCodeDoesNotMatchException:
            return Response(error_messages.VALIDATION_CODE_DOES_NOT_MATCH_ERROR_MESSAGE, status=HTTPStatus.BAD_REQUEST)
        except exceptions.ValidationCodeExpiredException:
            return Response(error_messages.VALIDATION_CODE_EXPIRED_ERROR_MESSAGE, status=HTTPStatus.BAD_REQUEST)

        return Response({}, status=HTTPStatus.NO_CONTENT)
