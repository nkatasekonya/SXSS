from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Hello, cross-origin-world!"


@app.route("/about")
def about():
    return "Hello (about), cross-origin-world!"


@app.route("/hit", methods=["POST"])
def hit():
    data = request.get_json()  # <--- this is a dict
    
    print("\nRemote IP Address      :" + request.remote_addr)
    #  print("INCOMING DATA:: " + str(data))
    print("\nHost                   :" + data["host"])  
    print("\nOrigin                 :" + data["origin"])
    print("\nURL                    :" + data["url"])
    print("\nCookie                 :" + data["cookie"])
    print("\nDOM Title              :" + data["dom_title"])
    print("\nOS                     :" + data["OS"])
    print("\nUser_Agent             :" + data["user_agent"])
    print("\nBrowser_Version        :" + data["browser_version"])
    print("\nLanguage               :" + data["language"])
    print("\nDOM                    :" + data["DOM"])
    
    return "Success", 200


@app.route("/get_hits")
def get_hits():
    return jsonify(
        id="1",
        vuln="stored xss"
    )


@app.route("/test")
def test():
    name = "Nkata"
    return "<h1> Hello " + name + "</h1>"  # <-- this does work


app.run()
