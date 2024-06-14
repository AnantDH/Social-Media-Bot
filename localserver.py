import http.server
import socketserver
import threading
import os

class Server:
    def __init__(self, port=8000):
        self.port = port
        self.handler = http.server.SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer(("", self.port), self.handler)
        self.server_thread = threading.Thread(target=self.httpd.serve_forever)
        self.server_thread.daemon = True

    def start_server(self):
        print(f"Starting server at http://localhost:{self.port}")
        self.server_thread.start()

    def shutdown_server(self):
        print("Shutting down server...")
        self.httpd.shutdown()
        self.httpd.server_close()
        self.server_thread.join()
        print("Server shut down.")

# Functions to start and stop the server
def start_server(port=8000):
    server = Server(port)
    server.start_server()
    return server

def shutdown_server(server):
    server.shutdown_server()
