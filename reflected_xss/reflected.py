import requests
import subprocess
from pyfiglet import figlet_format


def http_get(_link) -> tuple:
    req = requests.get(_link, cookies={'id': 'cookie'})
    return req.status_code, req.text


def http_post(_link, _data) -> tuple:
    req = requests.post(_link, data=_data, cookies={'id': 'cookie'})
    return req.status_code, req.text


def http_put(_link, _data) -> tuple:
    req = requests.put(_link, data=_data, cookies={'id': 'cookie'})
    return req.status_code, req.text


def format_endpoint(_endpoint: str, _payload: str) -> dict:
    formatted_endpoint = {"endpoint": _endpoint.replace("{payload}", _payload.replace("\"", "'")).replace("\n", ""),
                          "payload": _payload.replace("\"", "'").replace("\n", "")}
    return formatted_endpoint


def format_data(_post: dict, _payload: str, key) -> tuple:
    p = _payload.replace("\"", "'").replace("\n", "")
    for k in _post.keys():
        if _post[k] == "{payload}":
            _post[k] = p
            key = k
        else:
            _post[key] = p
    return _post, key


def fuzzing(_requests: list) -> list:
    success: list = []

    subprocess.run(["clear"])
    print("\u001b[31m" + figlet_format("SXSS", font="standard"))

    print("\u001b[36m [!] Fuzzing...")
    print("\u001b[31m ------------------------------------------------------------------------------------------------")

    for req in _requests:

        if req["method"].lower() == "get":
            with open("reflected_xss/payloads.db") as payloads:  # payloads.db
                for payload in payloads:
                    if "{payload}" in req["data"]:
                        formatted_endpoint = format_endpoint(req["data"], payload)
                        status_code, DOM = http_get(formatted_endpoint["endpoint"])

                        """
                        To verify the XSS vulnerability
                            1. We are checking if the requests was successful (status_code == 200)
                            2. If the original xss payload is present inside the DOM
                               > it's presence means that the payload was not filtered at all 
                            Read More: https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/07-Input_Validation_Testing/01-Testing_for_Reflected_Cross_Site_Scripting
                        """
                        if status_code == 200 and formatted_endpoint["payload"] in DOM: 
                            _passed: str = "\u001b[32m [passed]      "
                            print(_passed + format_str(formatted_endpoint["endpoint"]))
                            print()
                        else:
                            _failed: str = "\u001b[31m [failed]      "
                            print(_failed + format_str(formatted_endpoint["endpoint"]))
                            print()
            payloads.close()
        elif req["method"].lower() == "post":
            key = ""
            with open("reflected_xss/payloads.db") as payloads:  # payloads.db
                for payload in payloads:
                    _data, key = format_data(req["data"], payload, key)
                    status_code, DOM = http_post(req["endpoint"], _data)

                    if status_code == 200 and payload.replace("\"", "'").replace("\n", "") in DOM:
                        _passed: str = "\u001b[32m [passed]      "
                        print(_passed + format_str(req["endpoint"]))
                        print("      Payload: " + str(req["data"]))
                        print()
                    else:
                        _failed: str = "\u001b[31m [failed]      "
                        print(_failed + format_str(req["endpoint"]))
                        print("      Payload: " + str(req["data"]))
                        print()

            payloads.close()
        elif req["method"].lower() == "put":
            key = ""
            with open("reflected_xss/payloads.db") as payloads:  # payloads.db
                for payload in payloads:
                    _data, key = format_data(req["data"], payload, key)
                    status_code, DOM = http_put(req["endpoint"], _data)

                    if status_code == 200 and payload.replace("\"", "'").replace("\n", "") in DOM:
                        _passed: str = "\u001b[32m [passed]      "
                        print(_passed + format_str(req["endpoint"]))
                        print("      Payload: " + str(req["data"]))
                        print()
                    else:
                        _failed: str = "\u001b[31m [failed]      "
                        print(_failed + format_str(req["endpoint"]))
                        print("      Payload: " + str(req["data"]))
                        print()
            payloads.close()
    print("\u001b[31m ------------------------------------------------------------------------------------------------")
    return success
    
    
def format_str(_endpoint: str):
    if len(_endpoint) > 130:
        new_endpoint = _endpoint[0:130] + "\n               " + _endpoint[130:len(_endpoint)]
        return new_endpoint
    return _endpoint
   
