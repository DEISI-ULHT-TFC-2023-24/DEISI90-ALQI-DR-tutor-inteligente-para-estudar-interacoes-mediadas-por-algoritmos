import datetime

import requests
import json


# Function to append data to JSON file
def append_to_json(content, filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_headlines = {item['headline'] for item in existing_data}

    if content['headline'] not in existing_headlines:
        existing_data.append(content)
    else:
        print(f"Item with headline \"{content['headline']}\" already in JSON")

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)
    print(f"Data appended to {filename}")


# Function to fetch news data from the API
def fetch_news_data():
    url = "https://eco.sapo.pt/wp-json/eco/v1/items"
    response = requests.get(url)
    data = response.json()
    return data


def standardize_date(pub_date):
    date_string = "2024-04-18T07:57:04Z"

    date_object = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")

    formatted_date = date_object.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_date


if __name__ == "__main__":
    news_data = fetch_news_data()

    for item in news_data:
        if 'metadata' in item and 'tags' in item['metadata'] and item['metadata']['tags']:
            category = item['metadata']['tags'][0]['webTitle']
        else:
            continue

        published_date = standardize_date(item['pubDate'])
        data = {
            'headline': item['title']['long'],
            'source': "Sapo",
            'url': item['links']['webUri'],
            'content': [
                {
                    'type': 'text',
                    'data': item['body']
                }
            ],
            'published': published_date,
            'category': 'ultimas'  # Enquanto não houver um mapa de palavras para a categoria geral
        }

        # Check if there is an image URL
        if item.get('images') and isinstance(item['images'], dict) and item['images'].get('wide') and 'urlTemplate' in \
                item['images']['wide']:
            data['content'].append({
                'type': 'image',
                'data': item['images']['wide']['urlTemplate']
            })

        filename = f"data_scrapping/sapoApi/ultimas.json"
        append_to_json(data, filename)
