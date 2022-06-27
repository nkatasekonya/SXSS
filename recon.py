import re
import requests
import subprocess
from bs4 import BeautifulSoup
from pyfiglet import figlet_format


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

    for data in regex_url_compiled.findall(html):
        if data is not None:
            _endpoints.append(data)

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
        if link.startswith("/"):
            _formatted_urls.append(_url + "/" + link.removeprefix("/"))
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


def get_forms(_url: str):
    html = requests.get(_url).text
    soup = BeautifulSoup(html, 'html.parser')
    forms = soup.find_all(['form'])

    if forms:
        # subprocess.run(["clear"])
        # print("\u001b[31m" + figlet_format("SXSS", font="standard"))
        print("\n")
        print("\u001b[36m [!] Forms On: " + _url)
        print("\u001b[31m ------------------------------------------------------------------------------------------------")

        for form in forms:
            _endpoint_header: str =      "\u001b[32m [Endpoint]           "
            _method_header: str =        "\u001b[32m [HTTP Method]        "
            _form_elements_header: str = "\u001b[32m [Form Elements]      "

            print(_endpoint_header + _url + form['action'])
            print(_method_header + form['method'])
            print(_form_elements_header + str([(element['name'], element.get('value', '')) for element in form.find_all('input')]))
            print()

    print("\u001b[31m ------------------------------------------------------------------------------------------------")
