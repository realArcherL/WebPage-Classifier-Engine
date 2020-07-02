import json
import operator
import pathlib
import time


def button_maker(tag_id, button_id, what_list):
    start_string = f'<a class="btn btn-full" id="{button_id}" onclick="showText(\'{tag_id}\', \'{button_id}\')" ' \
                   f'href="javascript:void(0);">List of {what_list}</a>'
    return start_string


def list_maker(list_value, what_list, tag_id):
    string_list_value = f'<div id="{tag_id}" style="display:none;"><p><b>List Of {what_list}:</b></p>'
    if list_value:
        string_list_value += '<ul>'
        for value in list_value:
            string_list_value += f'<li>{value},&nbsp;</li>'

        string_list_value += '</ul></div>'
        return string_list_value
    else:
        string_list_value += 'None</div>'
        return string_list_value


def html_maker(content, path):
    css_data = '''<html>
    <head>
        <title>Web-Classifier</title>
        <style>
/*            main CSS */
            *{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            html{
                background-color: #fff;
                color: #555;
                font-family: 'Lato', 'Arial', sans-serif;
                font-weight: 300;
                font-size: 20px;
                text-rendering: optimizeLegibility;
                margin-left: 5px;
}

/*            resuable classes*/
            .row{
                max-width: 1140px;
                margin: 0 auto;
            }

            h2 {
                padding: 10;
                margin-left: 0 auto;
                width: 80%;
                float: left;
                margin-bottom: 40px;
                position: relative
            }

            .date{
                float: left;
                margin-left: 20px;
                padding: 5px;
                position: absolute;
                right: 14%;
                top: 7%;
                font-size: 20px;
                font-style: oblique
            }
/*            GRID*/
            .span_2_of_2 {
	           width: 100%;
            }

            .span_1_of_2 {
	           width: 49.2%;
            }


            /*  SECTIONS  ============================================================================= */

            .section {
	           clear: both;
	           padding: 0px;
	           margin: 0px;
}

            /*  GROUPING  ============================================================================= */


            .group:before,
            .group:after {
                content:"";
                display:table;
            }
            .group:after {
                clear:both;
            }
            .group {
                zoom:1; /* For IE 6/7 (trigger hasLayout) */
            }

            /*  GRID COLUMN SETUP   ==================================================================== */

            .col {
                display: block;
                float:left;
                margin: 1% 0 1% 1.6%;
            }

            .col:first-child { margin-left: 0; } /* all browsers except IE6 and lower */


            /*  REMOVE MARGINS AS ALL GO FULL WIDTH AT 480 PIXELS */

            @media only screen and (max-width: 480px) {
                .col {
                    margin: 1% 0 1% 0%;
                }
            }

/*  GO FULL WIDTH AT LESS THAN 480 PIXELS */

@media only screen and (max-width: 480px) {
	.span_2_of_2 {
		width: 100%;
	}
	.span_1_of_2 {
		width: 100%;
	}
}

/*            Navigation CSS*/
            .nav{
                margin: 0.1px;
                border: 1px solid white;
            }
            .nav li a{
                display: block;
                color: #fdfdfd;
                padding: 14px 16px;
                text-align: center;
                text-decoration: none;
            }
            .nav ul {
                list-style-type: none;
                margin: 0;
                padding: 0;
                overflow: hidden;
                background-color: #575454;
            }

            .nav li{
                float: left;
            }

            .nav li a:hover:not(.active){
                background-color: #6f5b5b;
            }

            .nav .active{
                background-color: #48698b;
            }
/*        Images    */
            .image-storage {
                width: 35%;
                margin: 0;
                float: left;
                background-color: rgba(180, 180, 180, 0.24);
                padding-bottom: 10px;
                margin-bottom: 40px;
            }
            .image-storage img {
                height: 250;
                width: 400;
                margin-top: 30px;
                margin-left: 12.5%;
                transition: 0.2s;
                border: 1px solid #575454;

            }

            .image-storage img:hover{
                transform: scale(1.25);
            }

            .description{
                padding: 15px;
                text-align: center;
                font-size: 16px;
                width: 100%;
            }

/*            Text*/
            .text-storage{
                float: left;
                width: 65%;
                padding-left: 5px;
            }

            .text-storage li {
                display: inline-block;
            }

/*            BUTTON*/
            .btn:link,
            .btn:visited
            {
                display: inline-block;
                padding: 5px 20px;
                font-size: 14px;
                text-decoration: none;
                border-radius: 200px;
                background-color: #48698b;
                color: white;
                transition: background-color 0.2s, border 0.2s, color 0.2s;
            }

            .btn-full:link,{
                background-color: #48698b;
                border: 1px solid #48698b;
                color: #fff;
                margin-right: 15px;
            }

            .btn-ghost:link,
            .btn-ghost:visited{
                color: White;
                padding: 5px;
                margin-bottom: 5px;
            }

            .btn-full:hover,
            .btn-full:active{
                border: 1px solid #e622b9;
                background-color: coral;
            }

            .btn-ghost:hover,
            .btn-ghost:active{
                background-color: red;
                color: #fff;
            }

        </style>
    </head>
    <body>
<!--        NAVIGATION BAR HTML-->
        <header>
            <div class="nav">
                <nav>
                    <ul>
                        <li><a href="#">WebPage-Classifier</a></li>
                        <li><a href="#">Stats</a></li>
                        <li style="float: right"><a class="active" href="#about"> About</a></li>
                    </ul>
                </nav>
            </div>
        </header>
'''
    html_creator = ""
    content.sort(key=operator.itemgetter('interest'), reverse=True)
    button_counter = 0
    text_counter = 0
    date_string = f'<h2 align="center">Total number of results: {len(content)} </h2><br><div class="date">Date: ' \
                  f'{time.ctime()}<br> Time: {time.strftime("%H:%M:%S")}</div>'

    # <!--IMAGE-->

    for query in content:
        # meta-data
        meta_string = f'''<div class="section description">
                    <a class="btn btn-ghost" href="#">Javascript enabled: {query['script']}</a>
                    <a class="btn btn-ghost" style="background: #eb00ff" href="#">Interest Value: {round(query['interest'], 2)}</a>
                    <a class="btn btn-ghost" style="background: #199b19" href="#">Port: {query['port']}</a>
                    <a class="btn btn-ghost" href="#">&nbsp;Is redirect: {query['is_redirect']}</a>
                    <a class="btn btn-ghost" style="background: #4747e0" href="{query['url']}" target="_blank">Open Link</a>
                    </div></div>'''

        # image-data
        image_path = query['image_path'][query['image_path'].find("Ima"):].strip()
        image_html = f'''<div class="section span_1_of_2 image-storage">
                <a href="{image_path}" target="_blank">
                    <img src="{image_path}" alt="{image_path}">
                </a>'''

        # opening html
        if query['is_redirect']:
            start_html = f'<div class="span_1_of_2 text-storage"><h4 align="centre"> URL: {query["url"]}<br>' \
                         f'Redirected from: {query["image_path"][query["image_path"].find("__"):].replace("__", "https://").replace(".png", "")}</h4>'
        else:
            start_html = f'<div class="span_1_of_2 text-storage"><h4 align="centre"> URL: {query["url"]}<br></h4>'

        # location list
        tag_id = 'tag_' + str(text_counter)
        button_id = 'btn_' + str(button_counter)
        data_string = list_maker(query['location_list'], 'Locations', tag_id) + '\n'
        button_string = button_maker(tag_id, button_id, 'Location') + '\n'
        button_counter += 1
        text_counter += 1

        # dates list
        tag_id = 'tag_' + str(text_counter)
        button_id = 'btn_' + str(button_counter)
        data_string += list_maker(query['dates_list'], 'Dates', tag_id) + '\n'
        button_string += button_maker(tag_id, button_id, 'Dates') + '\n'
        button_counter += 1
        text_counter += 1

        # organisation_list
        tag_id = 'tag_' + str(text_counter)
        button_id = 'btn_' + str(button_counter)
        data_string += list_maker(query['organisation_list'], 'Organisation', tag_id) + '\n'
        button_string += button_maker(tag_id, button_id, 'Organization') + '\n'
        button_counter += 1
        text_counter += 1

        # person_list
        tag_id = 'tag_' + str(text_counter)
        button_id = 'btn_' + str(button_counter)
        data_string += list_maker(query['person_list'], 'Names', tag_id) + '\n'
        button_string += button_maker(tag_id, button_id, 'Names') + '\n'
        button_counter += 1
        text_counter += 1

        # emails_list
        tag_id = 'tag_' + str(text_counter)
        button_id = 'btn_' + str(button_counter)
        data_string += list_maker(query['emails_list'], 'Emails', tag_id) + '\n'
        button_string += button_maker(tag_id, button_id, 'Emails') + '\n'
        button_counter += 1
        text_counter += 1

        # combo-basic list
        tag_id = 'tag_' + str(text_counter)
        button_id = 'btn_' + str(button_counter)
        data_string += list_maker(query['combo_basic'], 'Key Phrases', tag_id) + '\n'
        button_string += button_maker(tag_id, button_id, 'Key Phrases') + '\n'
        button_counter += 1
        text_counter += 1

        # # to add more options, just change the "based_on_functionality" in the below code"
        # tag_id = 'tag_' + str(text_counter)
        # button_id = 'btn_' + str(button_counter)
        # data_string += list_maker(query['based_on_functionality'], 'based_on_functionality', tag_id) + '\n'
        # button_string += button_maker(tag_id, button_id, 'based_on_functionality') + '\n'
        # button_counter += 1
        # text_counter += 1

        # headers
        tag_id = 'tag_' + str(text_counter)
        button_id = 'btn_' + str(button_counter)
        with open(query['headers_path'], 'r+') as file2:
            headers_data = json.load(file2)

        header_html = f'<div id="{tag_id}" style="display:none;">'
        for key, value in headers_data.items():
            header_html += f'<b>{key}</b> : {value}<br>'
        data_string += header_html + '</div>'
        button_string += button_maker(tag_id, button_id, 'Headers') + '\n'
        button_counter += 1
        text_counter += 1

        data_string += '</div>'
        script_html = '''<script language="JavaScript">
                function showText(id, btid){
                    var x = document.getElementById(id);
                    if (x.style.display === "none"){
                        x.style.display = "block";
                        document.getElementById(btid).style.backgroundColor = "#f25c5c";
                    } else{
                        x.style.display = "none";
                        document.getElementById(btid).style.backgroundColor = "#48698b";
                    }
                }
            </script>'''

        html_creator += image_html + '\n' + meta_string + '\n' + start_html + '\n' + button_string + '\n' + data_string \
                        + '\n' + script_html

    # print(html_creator)
    final_html = css_data + date_string + html_creator + '</body></html>'
    # print(final_html)

    with open(path / 'report.html', 'w+') as file3:
        file3.write(final_html)


def point_function(path):
    path = pathlib.Path(path)
    with open(path / 'final_1.json', 'r+') as file1:
        content = json.load(file1)
    html_maker(content, path)
    print('report_generated')


# point_function('2020-07-02_12')

