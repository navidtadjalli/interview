from http import HTTPStatus

from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.response import Response

from achare_interview.utils import exceptions, error_messages
from achare_interview.utils.registration_token import get_registration_token, validate_registration_token
from achare_interview.utils.validation_code import create_validation_code, validate_validation_code
from customer import serializers
from customer.models import Customer


class AuthenticateAPIView(generics.GenericAPIView):
    serializer_class = serializers.AuthenticateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number: str = serializer.validated_data.pop("phone_number")

        if Customer.objects.filter(phone_number=phone_number).exists():
            return Response({"can_login": True}, status=HTTPStatus.OK)

        create_validation_code(phone_number=phone_number)
        return Response(serializer.data, status=HTTPStatus.OK)


class ValidateAPIView(generics.GenericAPIView):
    serializer_class = serializers.ValidateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number: str = serializer.validated_data.pop("phone_number")

        try:
            validate_validation_code(
                phone_number=phone_number,
                code=serializer.validated_data.pop("code")
            )
        except exceptions.ValidationCodeDoesNotMatchException:
            return Response(error_messages.VALIDATION_CODE_DOES_NOT_MATCH_ERROR_MESSAGE, status=HTTPStatus.BAD_REQUEST)
        except exceptions.ValidationCodeExpiredException:
            return Response(error_messages.VALIDATION_CODE_EXPIRED_ERROR_MESSAGE, status=HTTPStatus.BAD_REQUEST)

        registration_token: str = get_registration_token(phone_number)

        return Response({"registration_token": registration_token}, status=HTTPStatus.OK)


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number: str = serializer.validated_data.pop("phone_number")

        try:
            validate_registration_token(
                phone_number=phone_number,
                token=serializer.validated_data.pop("registration_token")
            )
        except exceptions.RegistrationTokenIsNotValidException:
            return Response(error_messages.REGISTRATION_TOKEN_IS_NOT_VALID_ERROR_MESSAGE, status=HTTPStatus.BAD_REQUEST)

        Customer.objects.create_user(
            phone_number=phone_number,
            **serializer.validated_data
        )

        return Response({"token": "TOKEN"}, status=HTTPStatus.OK)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number: str = serializer.validated_data.pop("phone_number")
        password: str = serializer.validated_data.pop("password")

        if not Customer.objects.filter(phone_number=phone_number).exists():
            return Response(error_messages.PHONE_NUMBER_OR_PASSWORD_IS_INCORRECT_ERROR_MESSAGE,
                            status=HTTPStatus.BAD_REQUEST)

        customer: Customer = authenticate(request, phone_number=phone_number, password=password)
        if not customer:
            return Response(error_messages.PHONE_NUMBER_OR_PASSWORD_IS_INCORRECT_ERROR_MESSAGE,
                            status=HTTPStatus.BAD_REQUEST)

        return Response({"token": "TOKEN"}, status=HTTPStatus.OK)
