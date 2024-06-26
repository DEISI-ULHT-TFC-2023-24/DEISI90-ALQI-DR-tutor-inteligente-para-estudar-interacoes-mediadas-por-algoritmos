from news import views
from news.models import Source, Thread, Content, Category, Snippet, Option
import json
from django.db import connection


def import_json_data_RTP(json_data):
    with open(json_data, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for news_item in data:
        content_data = {
            'content_source_id': 1,
            'content_source': 'RTP',
            'content_headline': news_item['headline'],
            'content_url': news_item['url'],
            'content_category': news_item['category'],
            'content_text': news_item['content'][0]['data'],
            'content_image': news_item['content'][1]['data'],
            'content_date': news_item['published']
        }

        Content.objects.update_or_create(
            content_headline=news_item['headline'],
            defaults=content_data
        )


def import_json_data_NM(json_data):
    with open(json_data, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for news_item in data:
        content_data2 = {
            'content_source_id': 2,
            'content_source': "Noticias ao Minuto",
            'content_headline': news_item['headline'],
            'content_url': news_item['url'],
            'content_category': news_item['category'],
            'content_text': news_item['content'][0]['data'],
            'content_image': news_item['content'][1]['data'],
            'content_date': news_item['published']
        }

        Content.objects.update_or_create(
            content_headline=news_item['headline'],
            defaults=content_data2
        )


def import_json_data_sapo(json_data):
    with open(json_data, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for news_item in data:
        content_data3 = {
            'content_source_id': 3,
            'content_source': "Sapo",
            'content_headline': news_item['headline'],
            'content_url': news_item['url'],
            'content_category': news_item['category'],
            'content_text': news_item['content'][0]['data'],
            'content_date': news_item['published']
        }

        # Check if 'content' list has at least two elements and if 'data' exists in the second element
        if len(news_item['content']) > 1 and 'data' in news_item['content'][1]:
            content_data3['content_image'] = news_item['content'][1]['data']

        Content.objects.update_or_create(
            content_headline=news_item['headline'],
            defaults=content_data3
        )


def import_json_thread_response(json_data):
    with open(json_data, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for news_item in data:
        content_id_obj = views.get_content_id(news_item['content_title'])
        if content_id_obj is not None:
            content_id = (views.get_content_id(news_item['content_title'])).content_id
            thread_details = {detail['type']: detail['data'] for detail in news_item['thread_details']}
            content_data4 = {
                'content_id': content_id,
                'content_title': news_item['content_title'],
                'sentiment_valence': thread_details.get('sentiment_valence'),
                'style': thread_details.get('style'),
                'tone': thread_details.get('tone'),
                'keyword': thread_details.get('keyword')
            }

            thread_instance, created = Thread.objects.update_or_create(
                content_title=news_item['content_title'],
                defaults=content_data4
            )
            thread_id = thread_instance.thread_id

            snippets = news_item['thread_response'].split('\n')
            import_news_snippet(thread_id, snippets)


        else:
            print(f"Warning: Could not find content_id for '{news_item['content_title']}'")


def import_news_snippet(thread_id, snippets):
    for snippet in snippets:
        snippet = snippet.replace('\'', '')
        snippet_data = {
            'thread_id': thread_id,
            'snippet_text': snippet.replace('\'', ''),
            'time_to_consume': 0,
        }

        snippet_instance, created = Snippet.objects.update_or_create(
            snippet_text=snippet,
            defaults=snippet_data
        )
        snippet_id = snippet_instance.snippet_id

        import_news_options(snippet_id)


def import_news_options(snippet_id):
    options = {
        'snippet_id': snippet_id,
        'option_default': ["Mostrar Mais", "Outra Coisa", "Voltar"],
        'option_added': [""]
    }

    # Create or update the Option instance
    Option.objects.update_or_create(
        snippet_id=options['snippet_id'],
        defaults={
            'option_default': options['option_default'],
            'option_added': options['option_added'] or ['']  # Ensuring the type is consistent
        }
    )
