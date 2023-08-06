import webbrowser
import wikipedia
import requests
from googlesearch import search

def search_youtube(input):
    try:
        url = f"https://www.youtube.com/results?search_query={input}"
        s = webbrowser.open(url)
        return
    except Exception as e:
        return e

def search_google(input):
    try:
        url = f"https://www.google.com/search?q={input}"
        s = webbrowser.open(url)
        return
    except Exception as e:
        return e


def search_bing(input):
    try:
        url = f"https://www.bing.com/search?q={input}"
        s = webbrowser.open(url)
        return
    except Exception as e:
        return e

def search_duckgo(input):
    try:
        url = f"https://duckduckgo.com/?q={input}&hps=1&ia=web"
        s = webbrowser.open(url)
        return
    except Exception as e:
        return e

def search_wikipedia(input=str, set_lang=str, sentence=int):
    try:
        wikipedia.set_lang(set_lang) 
        s = wikipedia.summary(input, sentence)
        return s
    except:
        return "Pesquisa não encontrado"



def search_google_books(query, max_results=10):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={max_results}"
    response = requests.get(url)
    data = response.json()
    if "items" in data:
        return [item["volumeInfo"]["title"] for item in data["items"]]
    else:
        return []

def search_wikipedia_paginated(query, language="en", page=1, results_per_page=5):
    wikipedia.set_lang(language)
    offset = (page - 1) * results_per_page
    results = wikipedia.search(query, results=results_per_page, offset=offset)
    return results


def check_website_availability(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False



def search_news(keyword):
    query = f"{keyword} news"
    news_list = []

    for result in search(query):
        news_list.append(result)

    return news_list


def convert_currency(amount, from_currency, to_currency, api_key):
    base_url = "https://api.exchangeratesapi.io/latest"
    params = {
        "base": from_currency,
        "symbols": to_currency,
        "access_key": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            return data["error"]
        else:
            exchange_rate = data["rates"][to_currency]
            converted_amount = amount * exchange_rate
            return f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}"
    else:
        return "Erro ao obter taxas de câmbio."



from translate import Translator

def translate_text(text, source_language, target_language):
    translator = Translator(from_lang=source_language, to_lang=target_language)
    translation = translator.translate(text)
    return translation

