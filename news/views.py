import subprocess
from time import sleep

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from news.static.dbController import importJson as ij
from thread_handler.content_text_to_query import load_json_file as lj
from .models import Category, Source, Content


def index(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    date = request.GET.get('date')
    source = request.GET.get('source')

    obj = Content.objects.all()

    if query:
        obj = obj.filter(content_headline__icontains=query)

    if category:
        obj = obj.filter(content_category=category)

    if date:
        obj = obj.order_by(date)
    else:
        obj = obj.order_by('-content_date')

    if source:
        obj = obj.filter(content_source=source)

    context = {
        'obj': obj,
        'query': query,
        'category': category,
        'date': date,
        'source': source,
        'categories': Category.objects.all(),
        'sources': Source.objects.all(),
    }

    return render(request, "index.html", context)


def news_detail(request, news_id):
    obj = Content.objects.filter(pk=news_id)
    context = {
        "obj": obj
    }

    return render(request, "content.html", context)


def generate_category_and_date_link(category, date_type, query=None):
    url = reverse('index') + f'?category={category}&date={date_type}'
    if query:
        url += f'&q={query}'
    return url


@csrf_exempt
def execute_python_script(request):
    category = request.GET.get('category', 'ultimas')
    obj = Content.objects.filter(content_category=category).order_by('-content_date')
    context = {
        "obj": obj,
    }
    try:
        subprocess.run(["python", "data_scrapping/RTP/RTP_RSS_To_json.py"])
        sleep(6)
        list_possibilities = ["ultimas", "pais", "mundo", "desporto", "economia", "cultura", "videos", "audios",
                              "politica"]
        for x in list_possibilities:
            ij.import_json_data_RTP("data_scrapping/RTP/{cat}.json".format(cat=x))
            lj("data_scrapping/RTP/ultimas.json".format(cat=x))

        subprocess.run(["python", "data_scrapping/Noticias_ao_Minuto/NM_RSS_to_json.py"])
        list_possibilities = ["ultimas", "politica", "pais", "fama", "mundo", "tech", "lifestyle", "casa", "auto",
                              "casaMinuto", "autoMinuto", "desporto", "economia", "cultura"]

        for x in list_possibilities:
            ij.import_json_data_NM("data_scrapping/Noticias_ao_Minuto/{cat}.json".format(cat=x))

        subprocess.run(["python", "data_scrapping/sapoApi/sapo_api_to_json.py"])
        ij.import_json_data_sapo("data_scrapping/sapoApi/ultimas.json")

        ij.import_json_thread_response("thread_handler/thread_responses.json")

        return redirect('/')
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_content_id(content_headline):
    obj = Content.objects.all()
    x = obj.filter(content_headline=content_headline).first()
    return x
