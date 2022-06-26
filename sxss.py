from reflected_xss.reflected import perform_requests
from ui.ui import get_arguments

if __name__ == '__main__':
    args: dict = get_arguments()
    if args["d"] == "-d":
        perform_requests()
