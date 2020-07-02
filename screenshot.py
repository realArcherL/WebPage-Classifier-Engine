import json
import pathlib
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time


def screenshot_taker(url, path):

    # FOR chrome Web-driver (chromium)
    # chromedriver = 'chromedriver'
    # PROXY = "socks5://127.0.0.1:9050"  # IP:PORT or HOST:PORT
    # options = webdriver.ChromeOptions()
    # options.add_argument('--proxy-server=%s' % PROXY)
    # options.headless = True
    # driver = webdriver.Chrome(chromedriver, options=options)

    # FOR Firefox Web-driver (geckodriver)
    options = Options()
    profile = webdriver.FirefoxProfile()
    options.add_argument("--headless")
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.socks", '127.0.0.1')
    profile.set_preference("network.proxy.socks_port", 9050)
    profile.set_preference("network.proxy.socks_remote_dns", True)
    profile.update_preferences()
    driver = webdriver.Firefox(firefox_profile=profile, options=options)

    # common part
    driver.get(url)

    # s = lambda x: driver.execute_script('return document.body.parentNode.scroll' + x)
    driver.set_window_size(1024, 768)  # May need manual adjustment
    driver.find_element_by_tag_name('body').screenshot(path)
    driver.find_element_by_tag_name('body').screenshot(path)
    print(f'[{time.strftime("%H:%M:%S")}]....{url} --> SCREENSHOT OK')
    driver.quit()


if __name__ == '__main__':
    # reading json file for URLs
    path = sys.argv[1]
    path = pathlib.Path(path)
    with open(path / 'downloaded.json', 'r+') as download_json:
        content = json.load(download_json)

    for query in content:
        url = query['url']
        path = (query['image_path']).replace(" ", "")
        try:
            screenshot_taker(url, path)
        except Exception as ex:
            print(f'[=FAILED=],[{time.strftime("%H:%M:%S")}].....{ex}')

# URL = 'http://nzh3fv6jc6jskki3.onion/'

# how to run
# python3 scrennshot (foldername constaing json)
