from django.urls import path

from customer import views

urlpatterns = [
    path("api/authenticate", views.AuthenticateAPIView.as_view(), name="authenticate"),
    path("api/validate", views.ValidateAPIView.as_view(), name="validate"),
    path("api/register", views.RegisterAPIView.as_view(), name="register"),
    path("api/login", views.LoginAPIView.as_view(), name="login")
]
