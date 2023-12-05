from inertia import render


def list_todos(request):
    return render(request, "todos/list")


def create_todo(request):
    return render(request, "todos/create")
