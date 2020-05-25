### Library

1. [requests library](https://realpython.com/python-requests/) Tutorial. *For output use [f-strings](https://realpython.com/python-f-strings/)*

2. [requests-html](https://requests.readthedocs.io/projects/requests-html/en/latest/)

3. [How to use proxies with python](https://blog.scrapinghub.com/python-requests-proxy), [How to use TOR as proxy](https://www.sylvaindurand.org/use-tor-with-python/) 

### Methods
1. [How to check for tor IP and clearnet IP](https://stackoverflow.com/questions/30286293/make-requests-using-python-over-tor)
2. [source](https://gist.github.com/jefftriplett/9748036)
    Now, time for the red pill:

    The request module is not looking up the .onion domain via the socks proxy but via standard dns. Since there is no root onion domain provided by icann or other NIC operators your lookup goes off to the root dns servers then dies.

    The solution is to use the socks5h:// protocol in order to enable remote DNS resolving via the socks proxy in case the local DNS resolving process fails. Use [The Source Luke](https://github.com/kennethreitz/requests/blob/e3f89bf23c53b98593e4248054661472aacac820/requests/packages/urllib3/contrib/socks.py#L158).

### STAGE 1 Classification model (Authentication page, or what? check based on responses)
1. [How HTTP responses are good for identifying what page it is.](https://searchengineland.com/the-ultimate-guide-to-http-status-codes-and-headers-for-seo-302786)

2. 

### STAGE 2 CLssification based on Text (Help to determine what is it which is being talked about)
[Industrial classification of WebPages](https://towardsdatascience.com/industrial-classification-of-websites-by-machine-learning-with-hands-on-python-3761b1b530f1)
