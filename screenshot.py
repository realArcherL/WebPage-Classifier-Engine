import json
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
import time


def screenshot_taker(url, path):

    # FOR chrome Web-driver (chromium)
    chromedriver = 'chromedriver'
    PROXY = "socks5://127.0.0.1:9050"  # IP:PORT or HOST:PORT
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % PROXY)
    options.headless = True
    driver = webdriver.Chrome(chromedriver, options=options)

    # FOR Firefox Web-driver (geckodriver)
    # options = Options()
    # profile = webdriver.FirefoxProfile()
    # options.add_argument("--headless")
    # profile.set_preference("network.proxy.type", 1)
    # profile.set_preference("network.proxy.socks", '127.0.0.1')
    # profile.set_preference("network.proxy.socks_port", 9050)
    # profile.set_preference("network.proxy.socks_remote_dns", True)
    # profile.update_preferences()
    # driver = webdriver.Firefox(firefox_profile=profile, firefox_options=options)

    # common part
    driver.get(url)

    s = lambda x: driver.execute_script('return document.body.parentNode.scroll' + x)
    driver.set_window_size(s('Width'), s('Height'))  # May need manual adjustment
    driver.find_element_by_tag_name('body').screenshot(path)
    driver.find_element_by_tag_name('body').screenshot(path)
    print(f'[{time.strftime("%H:%M:%S")}]....{url} --> SCREENSHOT OK')
    driver.quit()


def screenshot_main(path):
    # reading json file for URLs
    with open(path / 'downloaded.json', 'r+') as download_json:
        content = json.load(download_json)

    for query in content:
        url = query['url']
        path = query['image_path']
        screenshot_taker(url, path)

# URL = 'http://nzh3fv6jc6jskki3.onion/'
# point_function('2020-06-23_18/downloaded.json')
# screenshot_taker(URL, 'web.png')
