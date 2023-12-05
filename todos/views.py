import json
from inertia import render
from django.shortcuts import redirect
from todos.models import Todo


def list_todos(request):
    todos = Todo.objects.all()

    return render(request, "todos/list", {"todos": todos})


def create_todo(request):
    return render(request, "todos/create")


def store_todo(request):
    data = json.loads(request.body)

    Todo.objects.create(name=data["name"])

    return redirect("/todos")
