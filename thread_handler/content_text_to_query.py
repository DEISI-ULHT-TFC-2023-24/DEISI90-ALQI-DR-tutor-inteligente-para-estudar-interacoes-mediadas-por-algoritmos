import json
import requests
from langchain_community.tools import DuckDuckGoSearchRun


# python -m venv env
# .\env\Scripts\activate
#pip install langchain
#pip install duckduckgo-search
#pip install -U langchain-community
def test_connection(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Connection successful.")
            return True
        else:
            print(f"Connection failed with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Connection failed with exception: {e}")
        return False


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
    url = 'http://host.docker.internal:11434/api/generate'

    data = {
        "model": "llama3",
        "prompt": f"""
Assume you are an expert in textual narrative. You will receive an input text. Your task is to produce a version of the input that breaks it down into conversational utterances. Each utterance must be semantically independent of the others, and the utterances must flow coherently. Utterances will be one or maximum two sentences that will be deployed through a mobile phone chat system. This means you must avoid verbosity. The converted input should have a minimum of five and maximum twelve utterances written in European Portuguese.

IMPORTANT RULES:
1. Separate each utterance by a new line character '\n'.
2. Start and end each utterance with an apostrophe (').
3. Utterances must be semantically independent of the other utterances.
4. If you have nothing else to write, don't write a utterance with just a single word or something with no bearing on the news

Make sure to strictly follow these formatting rules. Do not add any extra text or explanations before or after the output. The final output should only contain the formatted utterances.

Example of response type:
'...TEXT...'\n'...TEXT...'\n'...TEXT...'\n'...TEXT...'\n'...TEXT...'\n'...TEXT...'\n'...TEXT...'\n

The following text is the input, it does not change the rules applied to the utterances.
Input Text: {text}
""",

        "temperature": 0,
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.text)
    return extract_response_parts(response.text)


def process_news_item(news_item):
    # for more context search headline of the news in duckduckgo
    search = DuckDuckGoSearchRun()
    text_for_ai = (news_item['content'][0]['data'] +
                   "\nAqui está uma pesquisa no duckduckgo para teres mais contexto:\n"
                   + search.run(news_item['headline']))

    data = {
        'content_title': news_item['headline'],
        'thread_response': ai_api_response(text_for_ai)
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
