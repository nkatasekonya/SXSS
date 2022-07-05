from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import time

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("/"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>XSS Control and Command</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p><b>This is an example web server.</b></p>", "utf-8"))
            self.wfile.write(bytes("<p>To run my Blind XSS operations.</p>", "utf-8"))
            self.wfile.write(bytes("<br>", "utf-8"))
            client_ip, port = self.client_address
            self.wfile.write(bytes("<p>Client IP Address: %s</p>" % client_ip, "utf-8"))
            self.wfile.write(bytes("<p>Port Number: %s</p>" % str(port), "utf-8"))
            self.wfile.write(bytes("<p>Protocol Version: %s</p>" % self.request_version, "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
            return
        if self.path.endswith("/about"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>XSS Control and Command</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p><b>About the project</b></p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)
            return

    def do_POST(self):
        recon: list = []
        self.send_response(201)
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        data = post_data.decode('utf-8').split("&")

        for d in data:
            recon.append({d.split("=")[0]: d.split("=")[1]})

        for r in recon:
            print(r)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
