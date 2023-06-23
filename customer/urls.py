from django.urls import path

from customer import views

urlpatterns = [
    path("register", views.AuthenticateAPIView.as_view(), name="authenticate")
]
