import json
import html2text
import spacy
import pyate
import pathlib
from flashtext.keyword import KeywordProcessor

path_parent = pathlib.Path("Downloads")
present_keywords = []


def check_key(dictionary, key):
    if key in dictionary:
        # print(key)
        return True
    else:
        return False


def interest_calculator(interesting_meter, total_test_cases):
    interest_value = round(interesting_meter / total_test_cases, 2)
    return interest_value


def percentage1(dum0, dumx):
    try:
        ans = float(dumx) / float(dum0)
        ans = ans * 100
    except:
        return 0
    else:
        return ans


# the keywords
def list_value_matcher(list_defination, list_keywords):
    length = len(list_keywords)
    default_value = 0
    # handling the null condition
    if len(list_defination) and length >= 1:
        list_keywords = map(lambda x: x.lower(), list_keywords)
        # can be used for generating tags, as the variable present contains the names of the matched keywords.
        present = {i for i in list_keywords if any(j in i for j in list_defination)}
        global present_keywords
        present_keywords = list(present)
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
                     'Content-Disposition', 'Content-Security-Policy', 'Strict-Transport-Security', 'ETag']
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
        script_flag = {'script': True}
        interesting_meter = interesting_meter + 1

    # text to code comparison
    h = html2text.HTML2Text()
    h.ignore_links = True
    try:
        text = h.handle(html_content).replace('![', " ").replace(']', ' ').replace('--', '-').replace('*', ' ').replace(
            '__', ' ').replace("\n", "").replace('**', ' ').replace('*(', ' ')
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

    web_page_type = web_page_type_define(text)
    print(present_keywords)

    data_extraction = {
        'location_list': list(location),
        'person_list': list(person),
        'dates_list': list(dates),
        'organisation_list': list(org),
        'emails_list': list(emails),
        'combo_basic': phrase_list,
        'type': web_page_type,
        'tags': present_keywords
    }
    return data_extraction, interest_value


# THIS IS REDUNDANT Libarary call, makes the script slow, but until Spacy is understood properly
# def_webPage type determiner will require a trained algorithm.
def web_page_type_define(text):
    category_porn = ['child porn', 'porn', 'bdsm', 'sex', 'Porn', 'anal', 'underage porn', 'under 18 porn',
                     'sick porn' 'sex', 'pedo', 'sex market']
    category_market = ['Market', 'Buy', 'Credit card', 'payment', 'market', 'buy', 'sell', 'Sale',
                       'Consumer', 'buy anonymously', 'buy cheap', 'buy original', 'price', 'discount']
    category_tech = ['software', 'malware', 'hacking', 'hack', 'cybersecurity', 'cyber', 'underground hacker', 'real hacker',
                      'hacker for real', 'hacking tools', 'copmuter program', 'computer', 'cyber attack']
    category_blog = ['comment', 'subscribe', 'like', 'date', 'by user', 'login', 'comment here', 'leave a comment',
                      'blog', 'post', 'publish', 'write a post', 'Tag']

    # category_define = [] # remember to add it to keywords

    keywords = category_porn + category_market + category_blog + category_tech

    kp0 = KeywordProcessor()
    for word in keywords:
        kp0.add_keyword(word)
        kp1 = KeywordProcessor()
    for word in category_porn:
        kp1.add_keyword(word)
        kp2 = KeywordProcessor()
    for word in category_market:
        kp2.add_keyword(word)
        kp3 = KeywordProcessor()
    for word in category_tech:
        kp3.add_keyword(word)
        kp4 = KeywordProcessor()
    for word in category_blog:
        kp4.add_keyword(word)

    x = str(text)
    y0 = len(kp0.extract_keywords(x))
    y1 = len(kp1.extract_keywords(x))
    y2 = len(kp2.extract_keywords(x))
    y3 = len(kp3.extract_keywords(x))
    y4 = len(kp4.extract_keywords(x))

    total_matches = y0

    per1 = float(percentage1(y0, y1))
    per2 = float(percentage1(y0, y2))
    per3 = float(percentage1(y0, y3))
    per4 = float(percentage1(y0, y4))

    category = "Could't define"

    if y0 == 0:
        category = 'None'
    else:
        if per1 >= per2 and per1 >= per3 and per1 >= per4:
            category = 'porn'
        elif per2 >= per3 and per2 >= per1 and per2 >= per4:
            category = 'market'
        elif per3 >= per1 and per3 >= per2 and per3>= per4:
            category = 'tech'
        elif per4 >= per1 and per4 >= per2 and per4 >= per3:
            category = 'blog'

    return category


# the argument here will the URL query (first Json dictionary)
def web_classifier_core(url):
    # will be handled by point function during multiprocessing
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

        # print(url)

        if pathlib.Path.exists(path_parent / 'final_1.json'):
            print(url['url'])
            print(f'{url["html_path"]}')
            # add the condition here and take the whole function in the if loop

            with open(path_parent / 'final_1.json', 'r+') as file2:
                dict_final = json.load(file2)
                dict_final.append(url)
                file2.seek(0)
                json.dump(dict_final, file2)
        else:
            print(url['url'])
            print(f'{url["html_path"]}')
            with open(path_parent / 'final_1.json', 'w+') as file3:
                json.dump([url], file3)
    except Exception as ex:
        print(ex)


def point_function(path):
    print('Classifying web Page')
    global path_parent
    path_parent = pathlib.Path(path)

    with open(path_parent / 'downloaded.json', 'r+') as download_json:
        content = json.load(download_json)

    for url in content:
        web_classifier_core(url)

    print("All web pages classified")

    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     executor.map(web_classifier_core, content)

# will be called by point function

# point_function('2020-06-23_18')
