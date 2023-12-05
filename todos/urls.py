from django.urls import path

from todos import views

urlpatterns = [
    path("", views.list_todos, name="list_todos"),
    path("create", views.create_todo, name="create_todo"),
    path("store", views.store_todo, name="store_todo"),
]
