import requests
import html2text

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}


def runner():
    # r = requests.get("https://3g2upl4pq6kufc4m.onion/", proxies=proxies)
    r = requests.get("https://exmaple.com")
    html_code = r.content.decode('Utf-8')
    
    h = html2text.HTML2Text()  # Initializing object
    h.ignore_links = True  # Giving attributes
    try:
        text = h.handle(html_code)  # handling the HTML code
        text_from_html = text.replace("\n", " ")  # replacing next line char
        print(text_from_html)
    except Exception as e:
        print(e)
