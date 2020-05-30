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
    return port_service_couple


def point_function(target):
    scanned_ports = []
    port_numbers = [21, 22, 23, 24, 80, 81, 8080, 8081, 443, 55080, 11009, 4050, 6667]
    # port_numbers = [21]
    start_time = time.time()
    target = target.split("//")[-1].split("/")[0].replace("www.", " ").strip()
    for ports in port_numbers:
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
        # passing -1 by default if the port scan fails
        scanned_ports = [['443', 'https']]
        print(f'[=ERROR=] : {error1} found on {target}')
    print(f"[{time.strftime('%H:%M:%S')}]....Number of Ports open {number_of_port} on {target}, Scan Finished in "
          f"{round((end_time - start_time), 2)} second(s)\n")
    return scanned_ports
