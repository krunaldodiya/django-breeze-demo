from django.urls import path

from ws import views

urlpatterns = [
    path("", views.ws, name="ws"),
]
