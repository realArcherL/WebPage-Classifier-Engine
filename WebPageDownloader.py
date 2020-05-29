import pprint
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
    'http://3g2upl4pq6kufc4m.onion'
}


def web_page_downloader(target):
    scanned_ports = portScanner.point_function(target)
    port_list = [port_value[0] for port_value in scanned_ports]
    service_list = [i[1] for i in scanned_ports]

    for (port, service) in zip(port_list, service_list):
        if service == 'http':
            target = f'{target.replace("https://", "http://")}'
        # extra step to ensure if any link comes as http
        elif service == 'https':
            target = f'{target.replace("http://", "https://")}'

        url = f'{target}:{port}'
        try:
            req = requests.get(url=url, proxies=proxies, timeout=20)
            status_code = req.status_code
            headers_dict = req.headers
            headers = pprint.pformat(headers_dict)
            url_req = req.url
            is_redirect = False
            if req.history:
                is_redirect = True
            html_code = req.text
            print(f'{url} :{status_code}')

            # ADD path to images once the screenshot app is made.
            output_for_processing = {
                'url': url_req,
                'is_redirect': is_redirect,
                'html_response': status_code,
                'headers_path': f'{path_html}/{url.replace("/", "_")}.html',
                'html_path': f'{path_headers}/{url.replace("/", "_")}_header',
                'image_path': f'{path_headers}/{url.replace("/", "_")}.png'
            }

            with open(path_html / f'{url.replace("/", "_")}.html', 'w+') as file1:
                file1.write(html_code)

            # with open(path_images / "file1.png", 'w+') as file2:
            #     file2.write()

            with open(path_headers / f'{url.replace("/", "_")}_header', 'w+') as file3:
                file3.write(headers)

            print(output_for_processing)
        except Exception as e:
            print(e)


# add parameters path_html, path_headers, path_images as well
def point_function(url_list):
    path_images.mkdir(parents=True, exist_ok=True)
    path_html.mkdir(parents=True, exist_ok=True)
    path_headers.mkdir(parents=True, exist_ok=True)

    start_time = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(web_page_downloader, url_list)
    end_time = time.perf_counter()
    print(f'download and stacking ended in {round(end_time - start_time, 2)}')


point_function(url_list=list2)