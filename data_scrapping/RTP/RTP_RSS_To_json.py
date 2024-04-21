import threading

from bs4 import BeautifulSoup
import requests
import json
import datetime


def append_to_json(content, filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
            if not isinstance(existing_data, list):
                existing_data = [existing_data]
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_ids = {item['headline'] for item in existing_data}

    if isinstance(content, list):
        for item in content:
            if item['headline'] not in existing_ids:
                existing_data.append(item)
                existing_ids.add(item['headline'])
            else:
                print(f"Item \"{item['headline']}\" already in JSON")
    else:
        if content['headline'] not in existing_ids:
            existing_data.append(content)
            existing_ids.add(content['headline'])
        else:
            print(f"Item \"{content['headline']}\" already in JSON")

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)
    print(f"Data appended to {filename}")


def find_image(list_content):
    for url in list_content:
        if url.startswith('<img src="'):
            url = url.split('src="')[1]
            url = url.split('"')[0]
            return url


def standardize_date(pub_date):
    try:
        # Try parsing the date using the first format
        date_obj = datetime.datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
    except ValueError:
        try:
            # If parsing fails, try the second format
            date_obj = datetime.datetime.strptime(pub_date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # If parsing fails for both formats, return None
            return None
    # Format the date as needed
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")


def get_news_data(x):
    rtpCat = x
    while 1:
        # input("Introduza a categoria (\"ultimas\",\"pais\",\"mundo\",\"desporto\",\"economia\",\"cultura\",\"videos\",\"audios\")")
        if not rtpCat:
            rtpCat = "ultimas"
        if rtpCat not in list_possibilities:
            print(f'Não existe a categoria {rtpCat}')
        else:
            break

    if rtpCat == "ultimas":
        soup = BeautifulSoup(requests.get('https://www.rtp.pt/noticias/rss').content, 'html.parser')
    else:
        soup = BeautifulSoup(requests.get(f'https://www.rtp.pt/noticias/rss/{rtpCat}').content, 'html.parser')

    try:
        with open(f"./{rtpCat}.json", 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_ids = {item['headline'] for item in existing_data}

    for item in soup.find_all('item'):
        content = item.text.strip()
        list_content = content.split('\n')
        list_content = [line.lstrip() for line in list_content]

        findLink = [line for line in list_content if line.startswith('https://www.rtp.pt')]
        findLink2 = findLink[0]

        published_date = standardize_date(item.find('pubdate').string.strip())

        data = {
            'headline': item.find('title').text,
            'source': "RTP",
            'url': findLink2,
            'content': [
                {
                    'type': 'text',
                    'data': list_content[4] if len(list_content) > 4 and list_content[4] else "No content"
                },
                {
                    'type': 'image',
                    'data': find_image(list_content)
                }
            ],
            'published': published_date,
            'category': rtpCat

        }
        existing_data.append(data)

    passtrough = (existing_data, rtpCat)
    return passtrough


if __name__ == "__main__":
    list_possibilities = ["ultimas", "pais", "mundo", "desporto", "economia", "cultura", "videos", "audios", "politica"]


    def fetch_and_append(category):
        data = get_news_data(category)
        append_to_json(data[0], f"data_scrapping/RTP/{category}.json")


    threads = []
    for category in list_possibilities:
        thread = threading.Thread(target=fetch_and_append, args=(category,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
