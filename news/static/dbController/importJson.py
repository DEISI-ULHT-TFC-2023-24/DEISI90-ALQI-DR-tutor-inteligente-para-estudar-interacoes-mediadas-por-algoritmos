from news.models import Source, Thread, Content, Category
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
        content_data2 = {
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
            content_data2['content_image'] = news_item['content'][1]['data']

        Content.objects.update_or_create(
            content_headline=news_item['headline'],
            defaults=content_data2
        )

