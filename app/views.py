from django.shortcuts import render
from .models import News1


# Create your views here.
def index(request):
    obj = News1.objects.all()
    context = {
        "obj": obj
    }
    return render(request, "index.html", context)
