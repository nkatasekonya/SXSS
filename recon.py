import re
import requests
import subprocess
from bs4 import BeautifulSoup
from pyfiglet import figlet_format
import random


def extract_endpoints(_url: str) -> list:
    regex_url = r"""
        (?:
        (?<=['|"|=])[a-zA-Z0-9_/:-]{1,}/[a-zA-Z0-9_./-]{3,}(?:[?|#][^"|\']{0,}|)|                   # URLs
        [a-zA-Z0-9_/.:-]{1,}.(?:php|asp|aspx|jsp|json|action|html|js|txt|xml)(?:[?|#][^"|\']{0,})|  # URLs with d/f extension
        (?:(?<=['|"|=|:])/|\.\./|\./)[A-Za-z0-9_/.-]+|                                              # Paths like /,../,/./
        [a-zA-Z0-9_/-]{1,}/[a-zA-Z0-9_/-]{1,}\.(?:[a-zA-Z./]{1,}|action)(?:[\?|#][^"|']{0,}|)|      # Endpoints
        (?:https?|ftp|file)://[^,;:()"\n<>`'\s]+                                                    # URLs d/f protocols
        )
    """
    _endpoints: list = []
    html = requests.get(_url).text
    regex_url_compiled = re.compile(regex_url, re.VERBOSE)

    for e in regex_url_compiled.findall(html):
        if e is not None:
            _endpoints.append(e)

    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all(['iframe', 'script', 'link', 'a', 'form']):
        if link.get('href') is not None and link.get('href') not in _endpoints:
            _endpoints.append(link.get('href'))
        if link.get('src') is not None and link.get('src') not in _endpoints:
            _endpoints.append(link.get('src'))
        if link.get('action') is not None and link.get('action') not in _endpoints:
            _endpoints.append(link.get('action'))

    for script in re.findall(r'src\s*=\s*(?:"|\')[a-zA-Z0-9\!\#\$\&-\:\;\=\?-\[\]_~\|%\/]+(?:"|\')', html):
        if script.split('=')[1].strip('"') not in _endpoints:
            _endpoints.append(script.split('=')[1].strip('"'))

    return _endpoints


def get_formatted_urls(_url: str) -> list:
    _formatted_urls: list = []
    _endpoints: list = extract_endpoints(_url)

    for link in _endpoints:
        if link.endswith("#"):
            link = link.removesuffix("#")

        if link.startswith("/"):
            _formatted_urls.append(_url + "/" + link.removeprefix("/"))
        elif link.startswith("./"):
            _formatted_urls.append(_url + "/" + link.removeprefix("./"))
        elif link.startswith("http"):
            _formatted_urls.append(link)
        else:
            _formatted_urls.append(_url + "/" + link)

    return _formatted_urls


def display_urls(base_url: str, urls: list) -> None:
    subprocess.run(["clear"])
    print("\u001b[31m" + figlet_format("SXSS", font="standard"))

    print("\u001b[36m [!] Extracting Endpoints: " + base_url)
    print("\u001b[31m ------------------------------------------------------------------------------------------------")

    for url in urls:
        _header: str = "\u001b[32m [*]      "
        print(_header + str(url))


def get_forms(_url) -> list:
    formatted_data: list = []
    html = requests.get(_url).text
    soup = BeautifulSoup(html, 'html.parser')
    forms = soup.find_all(['form'])

    if forms:
        for form in forms:
            _action: str = form.get('action', "Not Found")
            _method: str = form.get('method', "Not Found")
            _inputs: list = []

            for _input in form.find_all('input'):
                _type = _input.get('type', '')
                if _type != 'hidden' and _type != 'submit' and _type != 'reset' and _type != 'button':
                    _inputs.append(
                                    {"name": _input.get('name', ''), "type": _type, "value": _input.get('value', '')})

            select_tags = form.find_all("select")
            if select_tags:
                for select in select_tags:
                    _options = select.find_all("option")
                    _value = ""
                    if _options:
                        _value = _options.__getitem__(random.randint(0, len(_options))).get("value", '')
                    _inputs.append({"name": select.get('name', ''), "type": select.get('type', ''), "value": _value})

            for textarea in form.find_all("textarea"):
                _inputs.append({"name": textarea.get('name', ''), "type": textarea.get('type', ''),
                                "value": textarea.get('value', '')})

            if _action == "#":
                _action = ""
            formatted_data.append({
                "action": _action,
                "method": _method,
                "inputs": _inputs
            })

    return formatted_data


def display_forms(forms, _url) -> None:
    if forms:
        print("\n")
        print("\u001b[36m [!] Forms On: " + _url)
        print(
            "\u001b[31m ------------------------------------------------------------------------------------------------")

        for form in forms:
            _endpoint_header: str = "\u001b[32m [Endpoint(s)]      "
            _method_header: str = "\u001b[32m [HTTP Method]      "
            _inputs_header: str = "\u001b[32m [Form Inputs]      "

            print(_endpoint_header + form["action"])
            print(_method_header + form["method"])
            print(_inputs_header + str([_input for _input in form["inputs"]]))
            print()

    print("\u001b[31m ------------------------------------------------------------------------------------------------")


def prepare_requests(_url: str):
    forms = get_forms(_url)
    _requests: list = []
    default_inputs = {
        "text": "default_text",
        "search": "default_search",
        "password": "DeFauLt_Pa33word",
        "email": "dummyemail@gmail.com",
        "color": "#ffffff",
        "date": "2022-06-23",
        "datetime-local": "2022-06-17T13:44",
        "file": "",
        "month": "2022-07",
        "number": "5",
        "range": "5",
        "tel": "0111010101",
        "time": "12:49",
        "url": "www.google.com",
        "week": "2022-W26"
    }

    for form in forms:

        if form["action"] == "Not Found":
            form["action"] = _url
        elif form["action"].startswith("/"):
            form["action"] = _url + form["action"]
        elif form["action"].startswith("./"):
            form["action"] = _url + "/" + form["action"].removeprefix("./")
        else:
            form["action"] = _url + "/" + form["action"]

        if form["method"].lower() == "get" or form["method"] == "Not Found":
            params = form["inputs"]
            #  http://localhost/tutorial/get.php?name=Mac&age=21
            get_payload: str = form["action"] + "?"
            _old: str = "old payload"
            for param in params:
                if _old == param["name"]:
                    continue
                if not get_payload.endswith("?"):
                    get_payload += "&"
                get_payload += param["name"] + "="
                if param["value"] == '':
                    if param["type"] == 'text' or param["type"] == 'email' or param["type"] == 'search' or param["type"] == 'textarea':
                        get_payload += "{payload}"
                    elif default_inputs[param["type"]]:
                        get_payload += default_inputs[param["type"]]
                    else:
                        get_payload += "{payload}"
                else:
                    get_payload += param["value"]
                _old = param["name"]
            _requests.append({"endpoint": form["action"], "method": 'get', "data": get_payload})

        elif form["method"].lower() == "post":
            params = form["inputs"]
            post_payload: dict = {}

            for param in params:
                if param["value"] == '':
                    if param["type"] == 'text' or param["type"] == 'email' or param["type"] == 'search' or param["type"] == 'textarea':
                        post_payload[param["name"]] = "{payload}"
                    elif default_inputs[param["type"]]:
                        post_payload[param["name"]] = default_inputs[param["type"]]
                    else:
                        post_payload[param["name"]] = "{payload}"
                else:
                    post_payload[param["name"]] = param["value"]

            _requests.append({"endpoint": form["action"], "method": form["method"], "data": post_payload})
        elif form["method"].lower() == "put":
            params = form["inputs"]
            put_payload: dict = {}

            for param in params:
                if param["value"] == '':
                    if param["type"] == 'text' or param["type"] == 'email' or param["type"] == 'search' or param["type"] == 'textarea':
                        put_payload[param["name"]] = "{payload}"
                    elif default_inputs[param["type"]]:
                        put_payload[param["name"]] = default_inputs[param["type"]]
                    else:
                        put_payload[param["name"]] = "{payload}"
                else:
                    put_payload[param["name"]] = param["value"]

            _requests.append({"endpoint": form["action"], "method": form["method"], "data": put_payload})

    return _requests
