# SXSS
SXSS is A CLI toolkit to detect and keep track of Blind [XSS](https://xss.js.org/#/). [Blind XSS](https://www.acunetix.com/websitesecurity/detecting-blind-xss-vulnerabilities/) is a type of Stored XSS 
where an attacker blindly deploys malicious scripts that will be triggered in other parts of the application. It can, for example be used to steal cookies from admin pages

***aside:*** *SXSS has be deployed and tested on [Linode](https://www.linode.com/), however can be deployed with any cloud provider*

## Installation
```
git clone https://github.com/nkatasekonya/SXSS.git
cd SXSS
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 ./sxss.py
```

## Usage
cd stored_xss
flask run --host=<<server_ip>>
- Update stored_xss/xss.js with the IP address of the server
