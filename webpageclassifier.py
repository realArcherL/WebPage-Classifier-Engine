import json
import html2text
import spacy
import pyate
import pathlib


def check_key(dictionary, key):
    if key in dictionary:
        # print(key)
        return True
    else:
        return False


def interest_calculator(interesting_meter, total_test_cases):
    interest_value = round(interesting_meter / total_test_cases, 2)
    return interest_value


# the keywords
def list_value_matcher(list_defination, list_keywords):
    length = len(list_keywords)
    default_value = 0
    # handling the null condition
    if len(list_defination) and length >= 1:
        list_keywords = map(lambda x: x.lower(), list_keywords)
        present = {i for i in list_keywords if any(j in i for j in list_defination)}
        return interest_calculator(len(present), length)
    else:
        return default_value


# https://flaviocopes.com/http-response-headers/#cache-control
def test_on_headers(path_header):
    total_test_cases = 7
    interesting_meter = 0

    with open(path_header, 'r+') as header_input_file:
        headers_dict = json.load(header_input_file)

    # checking if these headers are present in the file
    check_headers = ['Server', 'Content-Type', 'Last-Modified', 'Set-Cookie', 'WWW-Authenticate', 'Alt-Svc',
                     'Content-Disposition']
    for headers in check_headers:

        if check_key(headers_dict, headers):
            # checking if version number is disclosed
            if any(map(str.isdigit, headers)):
                interesting_meter = interesting_meter + 1

            # checking what is the content of the file
            elif headers_dict['Content-Type'] == 'text/html':
                pass
            else:
                interesting_meter = interesting_meter + 1

            interesting_meter = interesting_meter + 1

    # returning the interest value calculated back to the caller function
    interesting_meter = interest_calculator(interesting_meter, total_test_cases)
    return interesting_meter


def test_on_html(html_path):
    with open(html_path, 'r+') as html_file:
        html_content = html_file.read()

    interesting_meter = 0
    script_flag = {'script': False}
    total_test_value = 7

    # will return tag count for image, let the caller decide the interesting criteria? right now appending to meter
    if html_content.count("<img") >= 2:
        interesting_meter = interesting_meter + 2
    else:
        interesting_meter = interesting_meter + 1

    # checking for login screen or search bar
    input_tag_count = html_content.count("<input")
    if input_tag_count >= 2:
        interesting_meter = interesting_meter + 2
    else:
        interesting_meter = interesting_meter + 1

    # checking for javascript, hence the interesting meter is increased by 10
    if html_content.count("<script"):
        script_flag = {'script': False}
        interesting_meter = interesting_meter + 1

    # text to code comparison
    h = html2text.HTML2Text()
    h.ignore_links = True
    try:
        text = h.handle(html_content).replace("\n", "")
    except Exception as e:
        text = " "
        print(e)
    # print(text)
    text_to_code_percent = round(len(text) / len(html_content), 2)
    if text_to_code_percent <= 0.20:
        interesting_meter = interesting_meter + 1
    else:
        interesting_meter = interesting_meter + 2

    # calculating final interest value
    interest_value = interest_calculator(interesting_meter, total_test_value)

    return interest_value, script_flag, text


def information_extraction(text):
    # detect language

    # gather information
    nlp = spacy.load('en_core_web_lg')

    # directory where the keywords list is stored.
    # Country Keywords LIST, add the value to a text file and not here. also make the user type everything in Lowercase.
    directory_list = pathlib.Path(f'Key_List')

    with open(directory_list / 'location_list') as location_list_file:
        location_keywords = location_list_file.read().splitlines()

    with open(directory_list / 'person_list') as person_list_file:
        person_keywords = person_list_file.read().splitlines()

    with open(directory_list / 'dates_list') as dates_list_file:
        dates_keywords = dates_list_file.read().splitlines()

    with open(directory_list / 'org_list') as org_list_file:
        org_keywords = org_list_file.read().splitlines()

    with open(directory_list / 'emails_list') as emails_list_file:
        emails_keywords = emails_list_file.read().splitlines()

    location = set()
    person = set()
    dates = set()
    org = set()
    emails = set()

    doc = nlp(text)
    # Extracting the name of countries, organisations, DATES and organisation
    for entity in doc.ents:
        if entity.label_ == 'GPE':
            location.add(entity.text.lower())
        elif entity.label_ == 'PERSON':
            person.add(entity.text.lower())
        elif entity.label_ == 'DATE':
            dates.add(entity.text.lower())
        elif entity.label_ == 'ORG':
            org.add(entity.text.lower())

    # updating interest values
    interest_value = list_value_matcher(location, location_keywords)
    interest_value = interest_value + list_value_matcher(person, person_keywords)
    interest_value = interest_value + list_value_matcher(dates, dates_keywords)
    interest_value = interest_value + list_value_matcher(org, org_keywords)
    interest_value = interest_value + list_value_matcher(emails, emails_keywords)

    # extracting keywords
    try:
        combo_basic = pyate.combo_basic(text).sort_values(ascending=False)
        phrase_list = combo_basic.index.tolist()
    except Exception as ex:
        print(ex)
        phrase_list = ['Text too small to analyze']

    # extraction emails
    for token in doc:
        if token.like_email:
            emails.add(token.text)

    data_extraction = {
        'location_list': list(location),
        'person_list': list(person),
        'dates_list': list(dates),
        'organisation_list': list(org),
        'emails_list': list(emails),
        'combo_basic': phrase_list
    }
    return data_extraction, interest_value


# def_webPage type determiner will require a trained algorithm.

# the argument here will the URL query (first Json dictionary)
def web_classifier_core(path, path_parent):
    print('Classifying web Page')
    path_parent = pathlib.Path(path_parent)
    # will be handled by point function
    with open(path, 'r+') as download_json:
        content = json.load(download_json)

    # will be handled by point function during multiprocessing
    for url in content:
        try:
            # response header analysis (common in all the downloaded web pages)
            interest_value = test_on_headers(url['headers_path'])
            interim_interest_value, script_flag, text = test_on_html(url['html_path'])

            # interest value update
            interest_value = interim_interest_value + interest_value

            data_extraction, final_interest_value = information_extraction(text)

            # interest value update
            interest_value = final_interest_value + interest_value
            interest = {'interest': interest_value}

            # merging the data
            url.update(script_flag)
            url.update(interest)
            url.update(data_extraction)

            print(f'{url["html_path"]}')
            # print(url)

            if pathlib.Path.exists(path_parent / 'final_1.json'):
                with open(path_parent / 'final_1.json', 'r+') as file2:
                    dict_final = json.load(file2)
                    dict_final.append(url)
                    file2.seek(0)
                    json.dump(dict_final, file2)
            else:
                with open(path_parent / 'final_1.json', 'w+') as file3:
                    json.dump([url], file3)
        except Exception as ex:
            print(ex)

    print("web pages classified")


# will be called by point function
# web_classifier_core('test.json', '2020-06-23_16/Images')
