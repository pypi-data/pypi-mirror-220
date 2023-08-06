import webbrowser
import wikipedia

def search_youtube(input):
    url = f"https://www.youtube.com/results?search_query={input}"
    s = webbrowser.open(url)
    return

def search_google(input):
    url = f"https://www.google.com/search?q={input}"
    s = webbrowser.open(url)
    return


def search_bing(input):
    url = f"https://www.bing.com/search?q={input}"
    s = webbrowser.open(url)
    return

def search_duckgo(input):
    url = f"https://duckduckgo.com/?q={input}&hps=1&ia=web"
    s = webbrowser.open(url)
    return

def search_wikipedia(input=str, set_lang=str, sentence=int):
    wikipedia.set_lang(set_lang)
    s = wikipedia.summary(input, sentence)
    return s



    
