import pprint
import random
import subprocess
from time import sleep

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
    random_content = random.choice(Content.objects.all())
    random_content_id = random_content.content_id

    snippets = Snippet.objects.filter(thread_id=thread_news[0].thread_id)
    snippet_options = {snippet.snippet_id: Option.objects.filter(snippet_id=snippet.snippet_id) for snippet in snippets}

    context = {
        "random_content_id": random_content_id,
        "snippets": snippets if snippets else None,
        "snippet_options": snippet_options if snippet_options else None,
        "obj": obj,
        #"comments": comments,
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


@require_POST
def save_emoji(request):
    print(request.META.get('HTTP_COOKIE'))
    if request.method == 'POST':
        snippet_id = request.POST.get('snippet_id')
        emoji_text = request.POST.get('emoji_text')

        # Find the news option record for the given snippet_id
        try:
            news_option = Option.objects.get(snippet_id=snippet_id)

            # Get the current option_added array
            option_added = news_option.option_added

            # Append the new emoji to the option_added array
            option_added.append(emoji_text)

            # Update the Option object with the new option_added array
            news_option.option_added = option_added

            # Save the updated Option object
            news_option.save()

            return JsonResponse({'status': 'success'})

        except Option.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Snippet not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


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
            lj("data_scrapping/RTP/ultimas.json".format(cat=x))

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
