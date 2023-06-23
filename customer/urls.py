from django.urls import path

from customer import views

urlpatterns = [
    path("authenticate", views.AuthenticateAPIView.as_view(), name="authenticate"),
    path("validate", views.ValidateAPIView.as_view(), name="validate"),
    path("register", views.RegisterAPIView.as_view(), name="register")
    # path("login", views.ValidateAPIView.as_view(), name="validate")
]
