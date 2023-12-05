from inertia import render
from django.shortcuts import redirect


def list_todos(request):
    return render(request, "todos/list")


def create_todo(request):
    return render(request, "todos/create")


def store_todo(request):
    return redirect("/todos/create")
