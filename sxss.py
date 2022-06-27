from recon import get_formatted_urls, display_urls, get_forms
from reflected_xss.reflected import perform_requests
from stored_xss.stored import display_payloads
from ui.ui import get_arguments

if __name__ == '__main__':
    args: dict = get_arguments()

    # run: python3 sxss.py -l https://eve.uj.ac.za/login.php
    if args["l"] != "":
        formatted_urls: list = get_formatted_urls(args["l"])
        display_urls(args["l"], formatted_urls)
        get_forms(args["l"])

    # run: python3 sxss.py -d
    if args["d"] == "-d":
        perform_requests()

    # run: python3 sxss.py -g
    if args["g"] == "-g":
        display_payloads()
