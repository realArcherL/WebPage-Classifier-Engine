### Library

1. [requests library](https://realpython.com/python-requests/) Tutorial. *For output use [f-strings](https://realpython.com/python-f-strings/)*

2. [requests-html](https://requests.readthedocs.io/projects/requests-html/en/latest/)

3. [How to use proxies with python](https://blog.scrapinghub.com/python-requests-proxy), [How to use TOR as proxy](https://www.sylvaindurand.org/use-tor-with-python/) 

4. [html2test](https://pypi.org/project/html2text/) Requires python>=3.5

5. [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

#### Scanner
6. [PySocks](https://pypi.org/project/PySocks/). StackOverFlow [answer](https://tor.stackexchange.com/questions/716/how-to-connect-to-a-remote-socket-through-tor-in-python) with respect to the configuration.

### Methods
1. [How to check for tor IP and clearnet IP](https://stackoverflow.com/questions/30286293/make-requests-using-python-over-tor)
2. [source](https://gist.github.com/jefftriplett/9748036)
    Now, time for the red pill:

    The request module is not looking up the .onion domain via the socks proxy but via standard dns. Since there is no root onion domain provided by icann or other NIC operators your lookup goes off to the root dns servers then dies.

    The solution is to use the socks5h:// protocol in order to enable remote DNS resolving via the socks proxy in case the local DNS resolving process fails. Use [The Source Luke](https://github.com/kennethreitz/requests/blob/e3f89bf23c53b98593e4248054661472aacac820/requests/packages/urllib3/contrib/socks.py#L158).
    
3. [Manage writing big JSON files](https://stackoverflow.com/questions/39339044/how-to-write-large-json-data)

4. [Threading](https://www.youtube.com/watch?v=IEEhzQoKtQU) I/O threading process, waiting for network data.

5. [How to Handles requests library skillfully](https://stackabuse.com/the-python-requests-module/)
    descided to switch to [urllib3](https://urllib3.readthedocs.io/en/latest/user-guide.html) module because of more rhobustness. 

### Literature review
*Answers why a threaded port scanner won't work for port on websites. We need to thread the operations*
1. [AUG-2019 paper on Tor Extraction](https://dl.acm.org/ft_gateway.cfm?id=3341486&type=pdf) Language and port scanning.
2. [Tor port scanning](https://arxiv.org/pdf/1308.6768.pdf) Language and detection

### STAGE 1 Classification model (Authentication page, or what? check based on responses)
1. [How HTTP responses are good for identifying what page it is.](https://searchengineland.com/the-ultimate-guide-to-http-status-codes-and-headers-for-seo-302786)

2. 

### STAGE 2 CLssification based on Text (Help to determine what is it which is being talked about)
[Industrial classification of WebPages](https://towardsdatascience.com/industrial-classification-of-websites-by-machine-learning-with-hands-on-python-3761b1b530f1)
