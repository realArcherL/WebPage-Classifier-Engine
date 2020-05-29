import time
from tabulate import tabulate
import socket
import socks

# proxychains4 nmap -Pn -sT -v scyllabyeatabumx.onion

# Make sure that only domain link is present. no 'https/https' and no '/'
target1 = 'https://3g2upl4pq6kufc4m.onion/'


def port_scanner(target, port):
    reverse_proxy = "127.0.0.1"
    tor_port = 9050

    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, reverse_proxy, tor_port, True)
    socket.socket = socks.socksocket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    timeout_value = 100

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
    start_time = time.time()
    print(f'Scan Started: {time.ctime()}')
    target = target.split("//")[-1].split("/")[0].replace("www.", " ").strip()
    for ports in port_numbers:
        result = port_scanner(target, ports)
        time.sleep(1)
        if result:
            scanned_ports.append(result)

    end_time = time.time()

    table_headers = ["Ports", "Service"]
    if scanned_ports:
        print(tabulate(scanned_ports, headers=table_headers))
    else:
        error1 = "No open ports found."
        # passing 443 by default if the port scan fails
        scanned_ports = [['443', 'https']]
        print(error1)
    print("\nNumber of Ports open %s, Scan Finished in %.2f seconds\n" % (
        str(len(scanned_ports)), (end_time - start_time)))
    print()
    return scanned_ports


# point_function(target1)
# scanned_ports = [['80', 'http'], ['443', 'https']]
