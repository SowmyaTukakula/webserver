import http.server
import base64
import json
import time

PORT = 8080
PRIVATE_KEY_PATH = "private_key.pem"
PUBLIC_KEY_PATH = "public_key.pem"

with open(PRIVATE_KEY_PATH, 'r') as f:
    PRIVATE_KEY = f.read()

with open(PUBLIC_KEY_PATH, 'r') as f:
    PUBLIC_KEY = f.read()

kid = "my_kid"
expiry = int(time.time()) + 3600  # 1 hour expiry for the key

class JWKSHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/.well-known/jwk.json":
            if expiry < time.time():
                self.send_response(410)  # HTTP 410 Gone
                self.end_headers()
                return

            jwk = {
                "kty": "RSA",
                "kid": kid,
                "n": base64.b64encode(PUBLIC_KEY.encode()).decode(),
                "e": "AQAB"
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(jwk).encode())
        else:
            self.send_method_not_allowed()

    def do_POST(self):
        if self.path == "/auth":
            # Mock JWT without proper cryptographic signature
            payload = {
                "username": "userABC",
                "exp": time.time() + 3600
            }
            jwt_token = base64.b64encode(json.dumps(payload).encode()).decode()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"token": jwt_token}).encode())
        else:
            self.send_method_not_allowed()

    def send_method_not_allowed(self):
        self.send_response(405)  # Method Not Allowed
        self.end_headers()

    # Add these to handle unsupported methods
    def do_PUT(self):
        self.send_method_not_allowed()

    def do_DELETE(self):
        self.send_method_not_allowed()

    def do_PATCH(self):
        self.send_method_not_allowed()

    def do_HEAD(self):
        self.send_method_not_allowed()


if __name__ == "__main__":
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, JWKSHandler)
    print(f"Server started on port {PORT}")
    httpd.serve_forever()
