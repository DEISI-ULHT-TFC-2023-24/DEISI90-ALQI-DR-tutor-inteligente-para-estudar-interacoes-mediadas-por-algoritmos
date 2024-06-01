import random
import subprocess
from time import sleep

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from news.static.dbController import importJson as ij
from thread_handler.content_text_to_query import load_json_file as lj
from .models import Category, Source, Content, Thread, Snippet, Option
from .forms import CommentForm
from emoji import Emoji


def index(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    date = request.GET.get('date')
    source = request.GET.get('source')
    random_content_id = 0

    filters = {
        'q': query,
        'category': category,
        'date': date,
        'source': source,
    }

    filters = {k: v for k, v in filters.items() if v}
    query_string = "?" + "&".join([f"{k}={v}" for k, v in filters.items()])
    has_query_string = len(query_string) > 1
    query_string = query_string.replace("%20", "")
    query_string = query_string.replace("?", "&")

    obj = Content.objects.all()
    if obj:
        random_content = random.choice(obj)
        random_content_id = random_content.content_id

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

    paginator = Paginator(obj, 20)

    page_number = request.GET.get('page', 1)

    page_obj = paginator.get_page(page_number)

    context = {
        'random_content_id': random_content_id,
        'query_string': query_string,
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'sources': Source.objects.all(),
        'filters': filters,
        'has_query_string': has_query_string,
    }

    return render(request, "index.html", context)


def news_detail(request, news_id):
    obj = Content.objects.filter(pk=news_id)
    thread_news = Thread.objects.all()
    thread_news = thread_news.filter(content_id=obj[0].content_id)
    #comments = Comment.objects.filter(content_id=obj[0].content_id)
    random_content = random.choice(Content.objects.all())
    random_content_id = random_content.content_id

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_user = form.cleaned_data['comment_user']
            comment_text = form.cleaned_data['comment_text']
            #Comment.objects.create(content_id=news_id, comment_user=comment_user, comment_text=comment_text)
    else:
        form = CommentForm()

    snippets = Snippet.objects.all()
    snippets = snippets.filter(thread_id=thread_news[0].thread_id)

    context = {
        "random_content_id": random_content_id,
        "snippets": snippets,
        "obj": obj,
        #"comments": comments,
        "form": form
    }

    return render(request, "content.html", context)


def generate_category_and_date_link(category, date_type, query=None):
    url = reverse('index') + f'?category={category}&date={date_type}'
    if query:
        url += f'&q={query}'
    return url


def random_news(request):
    all_content = Content.objects.all()

    if not all_content:
        return redirect('index')

    random_content = random.choice(all_content)

    return news_detail(request, random_content.content_id)


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
        list_possibilities = ["ultimas", "pais", "mundo", "desporto", "economia", "cultura", "politica"]
        for x in list_possibilities:
            ij.import_json_data_RTP("data_scrapping/RTP/{cat}.json".format(cat=x))
            lj("data_scrapping/RTP/{cat}.json".format(cat=x))
        """
        subprocess.run(["python", "data_scrapping/Noticias_ao_Minuto/NM_RSS_to_json.py"])
        list_possibilities = ["ultimas", "politica", "pais", "mundo", "tech", "auto", "desporto", "economia", "cultura"]

        for x in list_possibilities:
            ij.import_json_data_NM("data_scrapping/Noticias_ao_Minuto/{cat}.json".format(cat=x))
            lj("data_scrapping/Noticias_ao_Minuto/{cat}.json".format(cat=x))

        subprocess.run(["python", "data_scrapping/sapoApi/sapo_api_to_json.py"])
        ij.import_json_data_sapo("data_scrapping/sapoApi/ultimas.json")

        """

        ij.import_json_thread_response("thread_handler/thread_responses.json")

        return redirect('/')
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_content_id(content_headline):
    obj = Content.objects.all()
    x = obj.filter(content_headline=content_headline).first()
    return x
