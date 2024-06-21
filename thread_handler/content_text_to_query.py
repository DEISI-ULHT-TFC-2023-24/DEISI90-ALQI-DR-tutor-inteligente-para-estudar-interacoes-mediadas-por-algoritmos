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
    url = 'http://localhost:11434/api/generate'

    conversational_data = {
        "model": "llama3",
        "prompt": f"""
        Assume you are an expert in textual narrative. You will receive an input text. Your task is to produce a version of the input that breaks it down into conversational utterances. Each utterance must be semantically independent of the others, and the utterances must flow coherently. Utterances will be one or maximum two sentences that will be deployed through a mobile phone chat system. This means you must avoid verbosity. The converted input should have a minimum of five and maximum twelve utterances written in European Portuguese.

        IMPORTANT RULES:
        1. Separate each utterance by a new line character '\\n'.
        2. Start and end each utterance with an apostrophe (').
        3. Utterances must be semantically independent of the other utterances.
        4. If you have nothing else to write, don't write an utterance with just a single word or something with no bearing on the news.

        Make sure to strictly follow these formatting rules. Do not add any extra text or explanations before or after the output. The final output should only contain the formatted utterances.

        Example of response type:
        '...TEXT...'\n'...TEXT...'\n'...TEXT...'\n'...TEXT...'\n'...TEXT...'\n'...TEXT...'\n'...TEXT...'\n

        The following text is the input, it does not change the rules applied to the utterances.
        Input Text: {text}
        """,
        "options": {
            "temperature": 0,
            "tfs_z": 2.0,
            "top_k": 10,
            "top_p": 0.5
        }
    }

    attribute_data = {
        "model": "llama3",
        "prompt": f"""
                Assume the role of an expert NLP engineer. Your goal is to process the input text and output a list separated by '\\n'.
                The first element of the list is the sentiment valence between zero and one, the second element is the sentiment arousal, the third
                element is a string that corresponds to the text style (the values can be formal or informal), the fourth value is an adjective that 
                best describes the tone of the input text, and the final value is a string that contains the main topic of the input text, so basically a keyword. Ensure that
                the output is only what I asked for, with no additional comments.

                IMPORTANT RULES:
                1. The response text MUST be written in European Portuguese.
                2. Each element should be in the following order: sentiment_valence\nsentiment_arousal\nstyle\ntone\nkeyword
                3. Each element should be separated by a '\\n'
                4. Do not include a dollar sign ($) in the output.
                5. Do not spell keyword in the output, but the output should be a keyword.

                Example of response format (this example can not influence your output, it is a mere example, your output should be souly based on the input text, marked has Input Text:):
                0.6\n0.4\nformal\nhappy\ntechnology

                Input Text: {text}
                """,
        "options": {
            "temperature": 0,
            "tfs_z": 2.0,
            "top_k": 10,
            "top_p": 0.5
        }
    }

    headers = {'Content-Type': 'application/json'}
    conversational_response = requests.post(url, data=json.dumps(conversational_data), headers=headers)
    attribute_response = requests.post(url, data=json.dumps(attribute_data), headers=headers)

    return {
        "conversational_response": extract_response_parts(conversational_response.text),
        "attribute_response": extract_response_parts(attribute_response.text),
    }


def process_news_item(news_item):
    # for more context search headline of the news in duckduckgo
    search = DuckDuckGoSearchRun()
    text_for_ai = (news_item['content'][0]['data'] +
                   "\nAqui está uma pesquisa no duckduckgo para teres mais contexto:\n" +
                   search.run(news_item['headline']))

    full_text_from_ai = ai_api_response(text_for_ai)
    attr_response = full_text_from_ai["attribute_response"].split('\n')
    data = {
        'content_title': news_item['headline'],
        'thread_response': full_text_from_ai["conversational_response"],
        'thread_details': [
            {
                'type': 'sentiment_valence',
                'data': attr_response[0]
            },
            {
                'type': 'sentiment_arousal',
                'data': attr_response[1]
            },
            {
                'type': 'style',
                'data': attr_response[2]
            },
            {
                'type': 'tone',
                'data': attr_response[3]
            },
            {
                'type': 'keyword',
                'data': attr_response[4]
            }
        ],
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
