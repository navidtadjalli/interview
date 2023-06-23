from django.urls import path

from customer import views

urlpatterns = [
    path("authenticate", views.AuthenticateAPIView.as_view(), name="authenticate"),
    path("validate", views.ValidateAPIView.as_view(), name="validate")
]
