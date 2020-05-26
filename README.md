## PROJECT WebPage-Classifier-Engine

[Introduction](#introduction)
1. Port Scanning(#port-scanning)
  



### Introduction
The project is basically to be able to create a core-classifier engine based on the paramteres like
1. HTTP responses (200 OK, 404, 301 etc)
2. What is the text, can it somehow be classified on that basis.

### Port Scanning
Port scanning on the onion link will help me assess the number of services it's running and help me decide which service to connect to.

The port_scanner is ```seprate function()``` can be called without the need of calling the ```point_function()```.
```python
def port_scanner(target, port):
    reverse_proxy = "127.0.0.1" # localhost.
    tor_port = 9050 # can be 9150, depends on your configuration.

    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, reverse_proxy, tor_port, True)
    socket.socket = socks.socksocket # Intialization of sockets for proxy.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    timeout_value = 100

    s.settimeout(timeout_value)
```
There is a reason why port scanning is performed on hardcoded port numbers, because the tor has a protection mechanism in place that rejects port scanning and thus a time delay was considered when coding the underlying part.

```
    port_numbers = [21, 22, 23, 24, 80, 443, 55080, 11009, 4050, 6667]
```
