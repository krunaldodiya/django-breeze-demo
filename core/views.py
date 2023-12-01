from inertia import render


# Create your views here.
def home(request):
    return render(request, "index")
