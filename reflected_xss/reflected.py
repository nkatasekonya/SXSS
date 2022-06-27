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
        if status_code == 200 and endpoint["payload"] in DOM:
            _passed: str = "\u001b[32m [passed]      "
            print(_passed + endpoint["endpoint"])
        else:
            _failed: str = "\u001b[31m [failed]      "
            print(_failed + endpoint["endpoint"])

    print("\u001b[31m ------------------------------------------------------------------------------------------------")
