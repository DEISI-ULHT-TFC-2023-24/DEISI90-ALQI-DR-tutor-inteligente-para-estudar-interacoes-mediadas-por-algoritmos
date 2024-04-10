import os
from time import sleep

from django.shortcuts import render, get_object_or_404

import news
from .models import Category, Source, Thread, Content
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
from news.static.dbController import importJson as ij
import data_scrapping.RTP


# Create your views here.
def index(request):
    category = request.GET.get('category', 'ultimas')
    obj = Content.objects.filter(content_category=category).order_by('-content_date')
    context = {
        "obj": obj,
    }
    return render(request, "index.html", context)


def news_detail(request, news_id):
    obj = Content.objects.filter(pk=news_id)
    context = {
        "obj": obj
    }

    return render(request, "content.html", context)


@csrf_exempt
def execute_python_script(request):
    category = request.GET.get('category', 'ultimas')
    obj = Content.objects.filter(content_category=category).order_by('-content_date')
    context = {
        "obj": obj,
    }
        # Run your Python script here
    try:
        subprocess.run(["python", "data_scrapping/RTP/RTP_RSS_To_json.py"])
        sleep(6)
        list_possibilities = ["ultimas", "pais", "mundo", "desporto", "economia", "cultura", "videos", "audios"]
        for x in list_possibilities:
            ij.import_json_data_RTP("data_scrapping/RTP/{cat}.json".format(cat=x))

        list_possibilities = ["ultimas", "politica", "pais", "fama", "mundo", "tech", "lifestyle", "casa", "auto",
                              "casaMinuto", "autoMinuto", "desporto", "economia", "cultura", "tudo"]

        for x in list_possibilities:
            ij.import_json_data_NM("data_scrapping/Noticias_ao_Minuto/{cat}.json".format(cat=x))

        return render(request, "index.html", context)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


