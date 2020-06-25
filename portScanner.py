import time
from tabulate import tabulate
import socket
import socks

"""
proxychains4 nmap -Pn -sT -v scyllabyeatabumx.onion
Made sure that only domain link is present. no 'https/https' and no '/'
"""


def port_scanner(target, port):
    reverse_proxy = "127.0.0.1"
    tor_port = 9050

    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, reverse_proxy, tor_port, True)
    socket.socket = socks.socksocket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    timeout_value = 25

    s.settimeout(timeout_value)
    port_service_couple = []
    try:
        s.connect((target, port))
        service_name = str(socket.getservbyport(port, "tcp"))

        port_service_couple.append(str(port))
        port_service_couple.append(service_name)
    except Exception as exception:
        print(f'[{time.strftime("%H:%M:%S")}]....{target}:{port} ==> {exception}')
        pass
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    return port_service_couple


def point_function(target):
    scanned_ports = []

    # PORT list based on Aquatone's core port scanner

    large_port_list = [80, 81, 443, 591, 2082, 2087, 2095, 2096, 3000, 8000, 8001,
                       8008, 8080, 8083, 8443, 8834, 8888]

    large_port_list2 = [80, 81, 300, 443, 591, 593, 832, 981, 1010, 1311,
                        2082, 2087, 2095, 2096, 2480, 3000, 3128, 3333, 4243, 4567,
                        4711, 4712, 4993, 5000, 5104, 5108, 5800, 6543, 7000, 7396,
                        7474, 8000, 8001, 8008, 8014, 8042, 8069, 8080, 8081, 8088,
                        8090, 8091, 8118, 8123, 8172, 8222, 8243, 8280, 8281, 8333,
                        8443, 8500, 8834, 8880, 8888, 8983, 9000, 9043, 9060, 9080,
                        9090, 9091, 9200, 9443, 9800, 9981, 12443, 16080, 18091, 18092,
                        20720, 28017]

    tor_port_numbers = [21, 22, 23, 24, 80, 81, 8080, 8081, 8443, 443, 55080, 11009, 4050, 6667]
    test_port_numbers = [80]

    start_time = time.time()
    target = target.split("//")[-1].split("/")[0].replace("www.", " ").strip()
    for ports in test_port_numbers:
        result = port_scanner(target, ports)
        time.sleep(1)
        if result:
            scanned_ports.append(result)

    end_time = time.time()
    number_of_port = len(scanned_ports)
    table_headers = ["Ports", "Service"]
    if scanned_ports:
        print(tabulate(scanned_ports, headers=table_headers))
    else:
        error1 = "No open ports found."
        # passing 443 by default if the port scan fails
        scanned_ports = [['443', 'https']]
        print(f'[=ERROR=] : {error1} found on {target}')
    print(f"[{time.strftime('%H:%M:%S')}]....Number of Ports open {number_of_port} on {target}, Scan Finished in "
          f"{round((end_time - start_time), 2)} second(s)\n")
    return scanned_ports
