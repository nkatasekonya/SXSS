from recon import get_formatted_urls, display_urls, get_forms, display_forms, prepare_requests
from reflected_xss.reflected import fuzzing
from stored_xss.stored import display_payloads
from ui.ui import get_arguments

if __name__ == '__main__':
    args: dict = get_arguments()

    # run: python3 sxss.py -l https://wikipedia.org
    if args["l"] != "":
        formatted_urls: list = get_formatted_urls(args["l"])
        display_urls(args["l"], formatted_urls)
        forms = get_forms(args["l"])
        display_forms(forms, args["l"])

    # run: python3 sxss.py -d https://wikipedia.org
    if args["d"] != "":
        reqs = prepare_requests(args["d"])
        fuzzing(reqs)

    # run: python3 sxss.py -g
    if args["g"] == "-g":
        display_payloads()
