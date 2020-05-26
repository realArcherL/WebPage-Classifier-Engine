## PROJECT WebPage-Classifier-Engine

[Introduction](#introduction)
1. [Port Scanning](#port-scanning)
    - [Literature](#literature)
    - [Performance](#performance)
  



### Introduction
The project is basically to be able to create a core-classifier engine based on the paramteres like
1. HTTP responses (200 OK, 404, 301 etc)
2. What is the text, can it somehow be classified on that basis.

### Port Scanning
#### Literature 
Port scanning on the onion link will help one assess the number of services it's running and decide which service to connect to.

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
There is a reason why port scanning is performed on hardcoded port numbers, because the tor has a protection mechanism in place that rejects port scanning whenever an unrecognized port is accessed and thus above mentioned condition and a time delay was considered when coding the scanner part. This is based on the [(2019)research paper's](https://dl.acm.org/doi/pdf/10.1145/3339252.3341486?download=true) finding.
The port numbers selected on the basis of this [(2014)study](https://arxiv.org/pdf/1308.6768.pdf) are mainly
SSH, HTTP(80), Skynet(Botnet, 55080), Tor Chat(11009), IRC(6667).

```
    port_numbers = [21, 22, 23, 24, 80, 443, 55080, 11009, 4050, 6667]
```
#### Performance

