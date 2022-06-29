from pyfiglet import figlet_format
import sys
import subprocess


def render_ui() -> None:
    # https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#8-colors
    # 31: RED, 32:GREEN, 36: BLUE

    subprocess.run(["clear"])

    print("\u001b[31m" + figlet_format("SXSS", font="standard"))

    print("\u001b[31m SXSS is A CLI toolkit to detect and keep track of Cross Site Scripting vulnerabilities")

    print("""
    \u001b[32m
    No   Name    Description
    ---  ----    -----------------------------
    [1]  -h:     help manual (getting started)
    [2]  -l:     extract endpoints from provided URL
    [3]  -d:     detect for XSS vulnerabilities
    [4]  -g:     generate XSS payloads
    """)


def help_manual() -> None:
    subprocess.run(["clear"])
    print("\u001b[32m" + figlet_format("SXSS", font="standard"))

    print("\u001b[32mNAME")
    print("\u001b[0m     SXSS is A CLI toolkit to detect and keep track of Cross Site Scripting vulnerabilities")

    print("\n\u001b[32mDESCRIPTION")
    print("\u001b[0m     SXSS is A CLI toolkit to detect and keep track of Blind XSS. Blind XSS is a type of Stored \n"
          "     XSS where an attacker blindly deploys malicious scripts that will be triggered in other \n"
          "     parts of the application. It can, for example be used to steal cookies from admin pages")

    print("\n\u001b[32mUSAGE")

    print("\u001b[0m     -l: extract endpoints from provided URL")
    print("\u001b[36m        python3 sxss.py -l http://example.com")
    print("\u001b[36m")

    print("\u001b[0m     -d: detect cross-site scripting vulnerabilities against provided endpoints")
    print("\u001b[36m        python3 sxss.py -d")
    print("\u001b[36m")

    print("\u001b[0m     -g: generate cross-site scripting payloads for a given URL")
    print("\u001b[36m        python3 sxss.py -g")
    print("\u001b[36m")

    print("\u001b[0m     -h: display the help page (manual)")
    print("\u001b[36m        python3 sxss.py -h")
    print("\u001b[36m")

    print("\n\u001b[32mAUTHOR")
    print("\u001b[0m     nkata sekonya (nkatasekonya61@gmail.com)")


def get_arguments() -> dict:
    """Get command line arguments (sys.argv returns a list with the first element being the name of the script"""
    args = {
        "l": "",
        "d": "",
        "g": "",
        "v": ""
    }

    index: int = 0
    for arg in sys.argv:

        if len(sys.argv) == 1:
            render_ui()
        elif arg == "-h":
            help_manual()
        elif arg == "-l":
            args["l"] = sys.argv.__getitem__(index+1)  # save URL
        elif arg == "-d":
            args["d"] = sys.argv.__getitem__(index+1)  # save URL
        elif arg == "-g":
            args["g"] = sys.argv.__getitem__(index)

        index += 1

    return args
