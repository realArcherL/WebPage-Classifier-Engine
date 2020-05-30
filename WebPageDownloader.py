import json
import requests
import concurrent.futures
import time
import pathlib
import portScanner

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# directory management
parent_directory = (time.strftime("%Y-%m-%d_%H"))
child_directory_1 = 'Images'
child_directory_2 = 'HTML'
child_directory_3 = 'Headers'
path1 = f'{parent_directory}/{child_directory_1}'
path2 = f'{parent_directory}/{child_directory_2}'
path3 = f'{parent_directory}/{child_directory_3}'
path_images = pathlib.Path(path1)
path_parent = pathlib.Path(parent_directory)
path_html = pathlib.Path(path2)
path_headers = pathlib.Path(path3)

list = {
    'https://github.com',
    'http://github.com',
    'https://google.com',
    'https://facebook.com',
    'https://duckduckgo.com',
    'https://guimp.com',

}
list2 = {
    'http://3g2upl4pq6kufc4m.onion/',
    'http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page',
    'http://idnxcnkne4qt76tg.onion',
    'http://torlinkbgs6aabns.onion',
    'http://jh32yv5zgayyyts3.onion',
    'http://wikitjerrta4qgz4.onion',
    'http://xdagknwjc7aaytzh.onion',
    'http://2vlqpcqpjlhmd5r2.onion',
    'http://nlmymchrmnlmbnii.onion',
    'http://wiki5kauuihowqi5.onion',
    'http://j6im4v42ur6dpic3.onion',
    'http://p3igkncehackjtib.onion',
    'http://kbhpodhnfxl3clb4.onion',
    'http://cipollatnumrrahd.onion'
}

list3 = {
    'https://idnxcnkne4qt76tg.onion'
}

list4 = {
    'http://3g2upl4pq6kufc4m.onion/',
}


def web_page_downloader(target):
    scanned_ports = portScanner.point_function(target)
    port_list = [port_value[0] for port_value in scanned_ports]
    service_list = [i[1] for i in scanned_ports]
    target = target.rstrip('/')
    for (port, service) in zip(port_list, service_list):
        if service == 'http':
            url = f'{target.replace("https://", "http://")}:{port}'
        # extra step to ensure if any link comes as http
        elif service == 'https':
            url = f'{target.replace("http://", "https://")}:{port}'

        try:
            req = requests.get(url=url, proxies=proxies, timeout=20)
            status_code = req.status_code
            headers = req.headers
            url_req = req.url
            is_redirect = False
            if req.history:
                is_redirect = True
            html_code = req.text
            print(f'[{time.strftime("%H:%M:%S")}]....Web page: {url} ==> {status_code}')

            # ADD path to images once the screenshot app is made.
            output_for_processing = {
                'url': url_req,
                'port': port,
                'is_redirect': is_redirect,
                'html_response': status_code,
                'headers_path': f'{path_html}/{url.replace("/", "_")}.html',
                'html_path': f'{path_headers}/{url.replace("/", "_")}_header.json',
                'image_path': f'{path_headers}/{url.replace("/", "_")}.png'
            }

            with open(path_html / f'{url.replace("/", "_")}.html', 'w+') as file1:
                file1.write(html_code)

            # with open(path_images / "file1.png", 'w+') as file2:
            #     file2.write()

            with open(path_headers / f'{url.replace("/", "_")}_header.json', 'w+') as file3:
                json.dump(dict(headers), file3)

            if pathlib.Path.exists(path_parent/'final.json'):
                with open(path_parent / 'final.json', 'r+') as file2:
                    dict_final = json.load(file2)
                    dict_final.append(output_for_processing)
                    file2.seek(0)
                    json.dump(dict_final, file2)
            else:
                with open(path_parent / 'final.json', 'w+') as file3:
                    json.dump([output_for_processing], file3)

        except Exception as e:
            with open(path_parent / 'failed.txt', 'a+') as file7:
                file7.write(f'{url} [=ERROR=] {e}\n')
            print(f'[=FAILED=],[{time.strftime("%H:%M:%S")}].....{e}')


# add parameters path_html, path_headers, path_images as well
def point_function(url_list):
    print(f'[{time.strftime("%H:%M:%S")}] Starting')
    path_images.mkdir(parents=True, exist_ok=True)
    path_html.mkdir(parents=True, exist_ok=True)
    path_headers.mkdir(parents=True, exist_ok=True)

    start_time = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(10) as executor:
        executor.map(web_page_downloader, url_list)
    end_time = time.perf_counter()
    print(f'\n[{time.strftime("%H:%M:%S")}].... Program ended in {round(end_time - start_time, 2)} second(s)')


# this main function is just for testing purposes
if __name__ == "__main__":
    try:
        point_function(url_list=list2)
    except KeyboardInterrupt:
        print("Press Ctr + C again")
        exit()
