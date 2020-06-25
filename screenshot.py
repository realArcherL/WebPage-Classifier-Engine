import json
from selenium import webdriver
import time


def screenshot_taker(url, path):
    PROXY = "socks5://127.0.0.1:9050"  # IP:PORT or HOST:PORT
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % PROXY)
    options.headless = True
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    s = lambda x: driver.execute_script('return document.body.parentNode.scroll' + x)
    driver.set_window_size(s('Width'), s('Height'))  # May need manual adjustment
    driver.find_element_by_tag_name('body').screenshot(path)
    driver.find_element_by_tag_name('body').screenshot(path)
    print(f'[{time.strftime("%H:%M:%S")}]....{url} --> SCREENSHOT OK')
    driver.quit()


def screenshot_main(path):
    # reading json file for URLs
    with open(path, 'r+') as download_json:
        content = json.load(download_json)

    for query in content:
        url = query['url']
        path = query['image_path']
        screenshot_taker(url, path)

# URL = 'http://nzh3fv6jc6jskki3.onion/'
# point_function('2020-06-23_18/downloaded.json')
# screenshot_taker(URL, 'web.png')
