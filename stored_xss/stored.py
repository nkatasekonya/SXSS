from stored_xss.config import config
import subprocess
from pyfiglet import figlet_format


def generate_payloads(payload_script: str) -> list:
    generated_payloads: list = []

    with open("stored_xss/payloads.db") as payloads:
        for payload in payloads:
            generated_payloads.append(payload.replace("{payload_script}", payload_script))
    payloads.close()

    return generated_payloads


def display_payloads(payload_script: str) -> None:
    payloads = generate_payloads(payload_script)

    subprocess.run(["clear"])
    print("\u001b[31m" + figlet_format("SXSS", font="standard"))

    print("\u001b[36m [!] Generating Payloads: " + config["script"])
    print("\u001b[36m ------------------------------------------------------------------------------------------------")
    for payload in payloads:
        _p: str = "\u001b[32m [payload]      "
        print(_p + payload)
    print("\u001b[36m ------------------------------------------------------------------------------------------------")
