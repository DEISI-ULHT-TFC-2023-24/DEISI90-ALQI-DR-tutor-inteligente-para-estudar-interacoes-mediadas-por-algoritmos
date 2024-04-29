import json
import requests


# Function to extract the 'response' field and concatenate them to form the complete message
def extract_response_parts(api_response_text):
    response_parts = api_response_text.split('\n')
    combined_response = ''.join(json.loads(part).get('response', '') for part in response_parts if part.strip())
    return combined_response


def insert_threaded_responses(content):
    try:
        with open("thread_handler/thread_responses.json", 'r', encoding='utf-8') as file:
            thread_responses_data = json.load(file)
    except FileNotFoundError:
        thread_responses_data = []

    thread_responses_data.extend(content)

    with open("thread_handler/thread_responses.json", 'w', encoding='utf-8') as file:
        json.dump(thread_responses_data, file, indent=4, ensure_ascii=False)


def ai_api_response(text):
    # for docker - http://host.docker.internal:11434/api/generate
    # for localhost - http://localhost:11434/api/generate
    url = 'http://localhost:11434/api/generate'
    data = {
        "model": "llama3",
        "prompt": f"Quero respostas com português de Portugal(nada de você, nem qualquer tipo de pronome, quero que seja tipo notícia). A partir de agora, vou dar apenas um texto de uma notícia e gostaria que fizesse um resumo, tipo thread de 300 palavras, quero que seja persuasivo e cativante. Aqui está o texto::\n{text}",
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.text)
    return extract_response_parts(response.text)


def process_news_item(news_item):
    data = {
        'content_title': news_item['headline'],
        'thread_response': ai_api_response(news_item['content'][0]['data'])
    }
    return data


def load_json_file(json_data):
    with open(json_data, 'r', encoding='utf-8') as file:
        json_news = json.load(file)

    with open("thread_handler/thread_responses.json", 'r', encoding='utf-8') as file:
        thread_responses_data = json.load(file)

    # Create a set of existing IDs in thread_responses.json
    existing_ids = set(response['content_title'] for response in thread_responses_data)

    threaded_response = []
    for news_item in json_news:
        headline = news_item['headline']
        if headline not in existing_ids:
            response = process_news_item(news_item)
            if response is not None:
                threaded_response.append(response)

    insert_threaded_responses(threaded_response)
