## PROJECT WebPage-Classifier-Engine

[Introduction](#introduction)
1. [Port Scanning](#port-scanning)
2. [Web Page donwloading](#web-page-downloading)
    - [Html](#html)
    - [Headers](#headers)
    - [image](#image)


### Introduction
The main aim of WebPage-Classifier-Engine is to be able to access, identify, and evaluate the.onion or clearnet web pages based on the keywords provided by the user. In addition, web pages are also evaluated based on their HTML properties such as the `HTML to text ratio`, the existence of certain `HTML headers` in the HTTP response of the website. The program applies request-library to fetch webpages and Pysocks library to interact with the Tor Linux library. For the classification of webpages, Spacy (Natural Language Processing) was employed.

### Installation
Download the tor library from your respective linux repository

```bash
sudo apt-get install tor
```

It would be wise to first set up a virtual environment and then install the requirements.txt. Once the `Spacy=2.2.4` has been installed, the spacy English language models must be installed `en_core_web_lg` & `en_core_web_sm`. (The essential language models are downloaded only after the requirements.txt has been installed, since the spacing=2.2.4 is required to run the project.)

```bash
python -m spacy en_core_web_lg
```

```bash
python -m spacy en_core_web_sm
```

### Usage
The program can be run using the bash script `run.sh`.

```bash
bash run.sh
```

The script executes Webpagedownloader.py which prompts for the path of the file containing the list of urls. The full working can be understood below.

### Port Scanning
Port scanning is performed via Pysocks library and only over selected ports, which is why port numbers are hard-coded port in the program itself. This is because tor has a protective mechanism in place that detects port scanning whenever an unrecognized port is accessed, thus considering the above-mentioned condition a time delay of one second was introduced while coding the part of the scanner and no threading was employed. This is based on the [(2019)research paper's](https://dl.acm.org/doi/pdf/10.1145/3339252.3341486?download=true) finding.

### Web Page donwloading
This being the parent script of all the scripts is called first when executing the `run.sh`. 
