## PROJECT WebPage-Classifier-Engine

[Introduction](#introduction)
[Installation](#installation)
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
