from django.shortcuts import render
from .models import Category, Source, Thread, Content


# Create your views here.
def index(request):
    obj = Content.objects.all()
    context = {
        "obj": obj
    }
    return render(request, "index.html", context)

