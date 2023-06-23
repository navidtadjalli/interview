from django.urls import path

from customer import views

urlpatterns = [
    path("register", views.RegisterAPIView.as_view(), name="register")
]
