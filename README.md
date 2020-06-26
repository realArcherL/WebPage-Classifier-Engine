## PROJECT WebPage-Classifier-Engine

[Introduction](#introduction)
1. [Port Scanning](#port-scanning)
    - [Literature](#literature)
    - [Performance](#performance)
2. [Web Page donwloading](#web-page-downloading)
    - [Html](#html)
    - [Headers](#headers)
    - [image](#image)


### Introduction
The main aim of WebPage-Classifier-Engine is to be able to access, identify, and evaluate the.onion or clearnet web pages based on the keywords provided by the user. In addition, web pages are also evaluated based on their HTML properties such as the `HTML to text ratio`, the existence of certain `HTML headers` in the HTTP response of the website. The program applies request-library to fetch webpages and Pysocks library to interact with the Tor Linux library. For the classification of webpages, Spacy (Natural Language Processing) was employed.

### Installation
Download the tor library from your respective linux repository

`sudo apt-get install tor`

It would be wise to first set up a virtual environment and then install the requirements.txt. Once the `Spacy=2.2.4` has been installed, the spacy English language models must be installed `en_core_web_lg` & `en_core_web_sm`. (The essential language models are downloaded only after the requirements.txt has been installed, since the spacing=2.2.4 is required to run the project.)

```bash
python -m spacy en_core_web_lg
```

```bash
python -m spacy en_core_web_sm
```

