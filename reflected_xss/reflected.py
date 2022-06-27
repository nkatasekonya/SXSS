import requests
import subprocess
from pyfiglet import figlet_format


# integrate auth: setting cookies or token
def http_get(_link) -> tuple:
    req = requests.get(_link)
    return req.status_code, req.text


def format_endpoint(_endpoint: str, _payload: str) -> dict:
    formatted_endpoint = {"endpoint": _endpoint.replace("{payload}", _payload.replace("\"", "'")).replace("\n", ""),
                          "payload": _payload.replace("\"", "'").replace("\n", "")}
    return formatted_endpoint


def prepare_requests() -> list:
    formatted_endpoints: list = []

    with open("reflected_xss/endpoints.txt") as endpoints:
        for endpoint in endpoints:
            with open("reflected_xss/payloads.db") as payloads:
                for payload in payloads:
                    formatted_endpoints.append(format_endpoint(endpoint, payload))
            payloads.close()
    endpoints.close()

    return formatted_endpoints


def perform_requests() -> None:
    endpoints: list = prepare_requests()

    subprocess.run(["clear"])
    print("\u001b[31m" + figlet_format("SXSS", font="standard"))

    print("\u001b[36m [!] Fuzzing...")
    print("\u001b[31m ------------------------------------------------------------------------------------------------")
    for endpoint in endpoints:
        status_code, DOM = http_get(endpoint["endpoint"])
        """
        To verify the XSS vulnerability
            1. We are checking if the requests was successful (status_code == 200)
            2. If the original xss payload is present inside the DOM
                > it's presence means that the payload was not filtered at all 
        Read More: https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/07-Input_Validation_Testing/01-Testing_for_Reflected_Cross_Site_Scripting
        """
        if status_code == 200 and endpoint["payload"] in DOM:
            _passed: str = "\u001b[32m [passed]      "
            print(_passed + endpoint["endpoint"])
        else:
            _failed: str = "\u001b[31m [failed]      "
            print(_failed + endpoint["endpoint"])

    print("\u001b[31m ------------------------------------------------------------------------------------------------")
