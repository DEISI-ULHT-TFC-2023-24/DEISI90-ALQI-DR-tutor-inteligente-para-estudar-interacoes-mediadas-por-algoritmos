from django.shortcuts import render
from .models import News


# Create your views here.
def index(request):
    obj = News.objects.all()
    context = {
        "obj": obj
    }
    return render(request, "index.html", context)
