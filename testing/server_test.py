# https://www.youtube.com/watch?v=RdSrkkrj3l4
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

#import http.server
#import socketserver

#PORT = 8000

#Handler = http.server.SimpleHTTPRequestHandler

#with socketserver.TCPServer(("", PORT), Handler) as httpd:
    #print("serving at port", PORT)
    #httpd.serve_forever()


from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client as client
import time

hostName = '0.0.0.0'
serverPort = 8000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "numbers")
        self.end_headers()
        print("hello")
        self.wfile.write(bytes("50/50"))
        return (50, 50)

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")